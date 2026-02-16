"""Toggl Track MCP server entry point."""

import os
import sys

from mcp.server.fastmcp import FastMCP

from toggl_client import TogglClient
from tools import register_read_tools, register_write_tools


def main() -> None:
    api_key = os.environ.get("TOGGL_API_KEY", "")
    if not api_key:
        print("Error: TOGGL_API_KEY environment variable is required", file=sys.stderr)
        sys.exit(1)

    mode = os.environ.get("TOGGL_MODE", "read").lower()
    transport = os.environ.get("TRANSPORT", "http").lower()
    port = int(os.environ.get("PORT", "9300"))

    mcp = FastMCP("Toggl Track")
    client = TogglClient(api_key)

    register_read_tools(mcp, client)

    if mode == "readwrite":
        register_write_tools(mcp, client)

    if transport == "stdio":
        mcp.run(transport="stdio")
    else:
        mcp.run(transport="streamable-http", host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
