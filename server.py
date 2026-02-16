"""Toggl Track MCP server entry point."""

import os

import uvicorn
from mcp.server.fastmcp import FastMCP

from toggl_client import TogglClient
from tools import register_read_tools, register_write_tools


class ClientHolder:
    """Mutable proxy around TogglClient.

    Passed to tool registration in place of a real client.
    Tools call holder.get() / holder.post() etc. — the holder delegates
    to the inner TogglClient which can be swapped at runtime when a new
    API key arrives via Authorization header.
    """

    def __init__(self, client: TogglClient | None = None, api_key: str = ""):
        self._client = client
        self._api_key = api_key

    def set_key(self, api_key: str) -> None:
        if api_key and api_key != self._api_key:
            self._client = TogglClient(api_key)
            self._api_key = api_key

    def _require(self) -> TogglClient:
        if self._client is None:
            raise RuntimeError(
                "No Toggl API key configured. "
                "Set TOGGL_API_KEY env var or send Authorization: Bearer <token> header."
            )
        return self._client

    # --- proxy every TogglClient method ---

    def get(self, path: str, params: dict | None = None) -> str:
        return self._require().get(path, params)

    def post(self, path: str, payload: dict | None = None) -> str:
        return self._require().post(path, payload)

    def put(self, path: str, payload: dict | None = None) -> str:
        return self._require().put(path, payload)

    def patch(self, path: str, payload: dict | None = None) -> str:
        return self._require().patch(path, payload)

    def delete(self, path: str) -> str:
        return self._require().delete(path)


class AuthMiddleware:
    """Pure ASGI middleware — extracts Bearer token from Authorization header."""

    def __init__(self, app, holder: ClientHolder):
        self.app = app
        self.holder = holder

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            for name, value in scope.get("headers", []):
                if name == b"authorization":
                    auth = value.decode()
                    if auth.startswith("Bearer "):
                        self.holder.set_key(auth[7:])
                    break
        await self.app(scope, receive, send)


def main() -> None:
    api_key = os.environ.get("TOGGL_API_KEY", "")
    mode = os.environ.get("TOGGL_MODE", "read").lower()
    transport = os.environ.get("TRANSPORT", "http").lower()
    port = int(os.environ.get("PORT", "9300"))

    holder = ClientHolder()
    if api_key:
        holder.set_key(api_key)

    mcp = FastMCP("Toggl Track", host="0.0.0.0", port=port)

    register_read_tools(mcp, holder)

    if mode == "readwrite":
        register_write_tools(mcp, holder)

    if transport == "stdio":
        mcp.run(transport="stdio")
    else:
        app = mcp.streamable_http_app()
        app = AuthMiddleware(app, holder)
        uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
