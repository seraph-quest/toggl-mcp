"""Workspace read tools."""

from mcp.server.fastmcp import FastMCP

from toggl_client import TogglClient


def register_read(mcp: FastMCP, client: TogglClient) -> None:
    @mcp.tool()
    def toggl_list_workspaces() -> str:
        """List all workspaces the authenticated user belongs to."""
        return client.get("/api/v9/workspaces")

    @mcp.tool()
    def toggl_get_workspace(workspace_id: int) -> str:
        """Get details of a specific workspace.

        Args:
            workspace_id: The workspace ID.
        """
        return client.get(f"/api/v9/workspaces/{workspace_id}")

    @mcp.tool()
    def toggl_list_workspace_users(workspace_id: int) -> str:
        """List all users in a workspace.

        Args:
            workspace_id: The workspace ID.
        """
        return client.get(f"/api/v9/workspaces/{workspace_id}/users")


def register_write(mcp: FastMCP, client: TogglClient) -> None:
    pass  # No write tools in this module
