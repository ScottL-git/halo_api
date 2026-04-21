"""Small GraphQL client module."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class GraphQLError(Exception):
    """Raised when a GraphQL request fails or returns GraphQL errors."""


@dataclass(slots=True)
class GraphQLClient:
    """Simple HTTP GraphQL client using the Python standard library."""

    endpoint: str
    timeout: float = 10.0
    headers: dict[str, str] | None = None

    def execute(self, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        """Execute a GraphQL query and return the ``data`` payload."""

        payload: dict[str, Any] = {"query": query, "variables": variables or {}}
        request_headers = {"Content-Type": "application/json", **(self.headers or {})}
        request = Request(
            self.endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers=request_headers,
            method="POST",
        )

        try:
            with urlopen(request, timeout=self.timeout) as response:
                body = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            raise GraphQLError(f"HTTP error from GraphQL endpoint: {exc}") from exc
        except URLError as exc:
            raise GraphQLError(f"Network error while calling GraphQL endpoint: {exc}") from exc

        if "errors" in body and body["errors"]:
            raise GraphQLError(f"GraphQL errors: {body['errors']}")

        return body.get("data", {})
