"""Centralized HTTP client for Toggl Track API."""

import json
from base64 import b64encode

import httpx

MAX_RESPONSE_CHARS = 50_000


class TogglClient:
    """Toggl API client with Basic auth and error handling."""

    BASE_URL = "https://api.track.toggl.com"

    def __init__(self, api_key: str):
        token = b64encode(f"{api_key}:api_token".encode()).decode()
        self._client = httpx.Client(
            base_url=self.BASE_URL,
            headers={
                "Authorization": f"Basic {token}",
                "Content-Type": "application/json",
            },
            timeout=30.0,
        )

    def _truncate(self, text: str) -> str:
        if len(text) > MAX_RESPONSE_CHARS:
            return text[:MAX_RESPONSE_CHARS] + "\n... (truncated)"
        return text

    def _handle_response(self, resp: httpx.Response) -> str:
        if resp.status_code == 204:
            return json.dumps({"success": True})
        try:
            resp.raise_for_status()
        except httpx.HTTPStatusError:
            return json.dumps({"error": f"HTTP {resp.status_code}: {resp.text}"})
        return self._truncate(resp.text)

    def get(self, path: str, params: dict | None = None) -> str:
        try:
            resp = self._client.get(path, params=params)
        except httpx.HTTPError as e:
            return json.dumps({"error": str(e)})
        return self._handle_response(resp)

    def post(self, path: str, payload: dict | None = None) -> str:
        try:
            resp = self._client.post(path, json=payload)
        except httpx.HTTPError as e:
            return json.dumps({"error": str(e)})
        return self._handle_response(resp)

    def put(self, path: str, payload: dict | None = None) -> str:
        try:
            resp = self._client.put(path, json=payload)
        except httpx.HTTPError as e:
            return json.dumps({"error": str(e)})
        return self._handle_response(resp)

    def patch(self, path: str, payload: dict | None = None) -> str:
        try:
            resp = self._client.patch(path, json=payload)
        except httpx.HTTPError as e:
            return json.dumps({"error": str(e)})
        return self._handle_response(resp)

    def delete(self, path: str) -> str:
        try:
            resp = self._client.delete(path)
        except httpx.HTTPError as e:
            return json.dumps({"error": str(e)})
        return self._handle_response(resp)
