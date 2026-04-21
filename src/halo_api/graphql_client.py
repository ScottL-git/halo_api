"""Simple GraphQL client module."""

from __future__ import annotations

import json
from typing import Any
from urllib import request


class _UrllibSession:
    """Small HTTP transport to mimic a session-style API without external deps."""

    def __init__(self, headers: dict[str, str] | None = None) -> None:
        self.headers = headers or {}

    def post(self, url: str, json_payload: dict[str, Any], timeout: int) -> dict[str, Any]:
        body = json.dumps(json_payload).encode("utf-8")
        req = request.Request(url=url, data=body, method="POST")
        req.add_header("Content-Type", "application/json")
        for key, value in self.headers.items():
            req.add_header(key, value)

        with request.urlopen(req, timeout=timeout) as response:  # noqa: S310
            payload = response.read().decode("utf-8")
            return json.loads(payload)


class GraphQLClient:
    """A lightweight GraphQL HTTP client."""

    def __init__(self, endpoint: str, headers: dict[str, str] | None = None, timeout: int = 30) -> None:
        self.endpoint = endpoint
        self.timeout = timeout
        self.session = _UrllibSession(headers=headers)

    def execute(self, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        """Execute a GraphQL query and return the parsed JSON response."""
        payload = {"query": query, "variables": variables or {}}
        data = self.session.post(self.endpoint, json_payload=payload, timeout=self.timeout)
        if "errors" in data and data["errors"]:
            raise ValueError(f"GraphQL errors returned: {data['errors']}")
        return data
