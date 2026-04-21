from halo_api import GraphQLClient


class DummySession:
    def __init__(self, payload: dict):
        self._payload = payload
        self.last_url = None
        self.last_json = None
        self.last_timeout = None

    def post(self, url: str, json_payload: dict, timeout: int) -> dict:
        self.last_url = url
        self.last_json = json_payload
        self.last_timeout = timeout
        return self._payload


def test_execute_success() -> None:
    client = GraphQLClient("https://example.test/graphql", headers={"Authorization": "Bearer abc"}, timeout=10)
    dummy = DummySession({"data": {"viewer": {"id": "1"}}})
    client.session = dummy

    result = client.execute("query { viewer { id } }")

    assert result == {"data": {"viewer": {"id": "1"}}}
    assert dummy.last_url == "https://example.test/graphql"
    assert dummy.last_json == {"query": "query { viewer { id } }", "variables": {}}
    assert dummy.last_timeout == 10


def test_execute_raises_on_graphql_errors() -> None:
    client = GraphQLClient("https://example.test/graphql")
    client.session = DummySession({"errors": [{"message": "bad request"}]})

    try:
        client.execute("query { bad }")
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "GraphQL errors returned" in str(exc)
