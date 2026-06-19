import json
from unittest.mock import Mock, patch
from urllib.error import URLError

import pytest

from halo_api.graphql_client import GraphQLClient, GraphQLError


def test_execute_returns_data_on_success():
    client = GraphQLClient("https://example.com/graphql", headers={"Authorization": "Bearer token"})

    response_mock = Mock()
    response_mock.read.return_value = json.dumps({"data": {"viewer": {"id": "123"}}}).encode("utf-8")
    response_mock.__enter__ = Mock(return_value=response_mock)
    response_mock.__exit__ = Mock(return_value=None)

    with patch("halo_api.graphql_client.urlopen", return_value=response_mock) as urlopen_mock:
        result = client.execute("query { viewer { id } }")

    assert result == {"viewer": {"id": "123"}}
    assert urlopen_mock.called


def test_execute_raises_graphql_error_when_response_has_errors():
    client = GraphQLClient("https://example.com/graphql")

    response_mock = Mock()
    response_mock.read.return_value = json.dumps({"errors": [{"message": "Boom"}]}).encode("utf-8")
    response_mock.__enter__ = Mock(return_value=response_mock)
    response_mock.__exit__ = Mock(return_value=None)

    with patch("halo_api.graphql_client.urlopen", return_value=response_mock):
        with pytest.raises(GraphQLError, match="GraphQL errors"):
            client.execute("query { broken }")


def test_execute_raises_graphql_error_on_network_failure():
    client = GraphQLClient("https://example.com/graphql")

    with patch("halo_api.graphql_client.urlopen", side_effect=URLError("connection lost")):
        with pytest.raises(GraphQLError, match="Network error"):
            client.execute("query { viewer { id } }")
