"""Client read + write tools."""

from mcp.server.fastmcp import FastMCP

from toggl_client import TogglClient


def register_read(mcp: FastMCP, client: TogglClient) -> None:
    @mcp.tool()
    def toggl_list_clients(workspace_id: int) -> str:
        """List all clients in a workspace.

        Args:
            workspace_id: The workspace ID.
        """
        return client.get(f"/api/v9/workspaces/{workspace_id}/clients")

    @mcp.tool()
    def toggl_get_client(workspace_id: int, client_id: int) -> str:
        """Get a specific client.

        Args:
            workspace_id: The workspace ID.
            client_id: The client ID.
        """
        return client.get(
            f"/api/v9/workspaces/{workspace_id}/clients/{client_id}"
        )


def register_write(mcp: FastMCP, client: TogglClient) -> None:
    @mcp.tool()
    def toggl_create_client(workspace_id: int, name: str) -> str:
        """Create a new client in a workspace.

        Args:
            workspace_id: The workspace ID.
            name: Client name.
        """
        return client.post(
            f"/api/v9/workspaces/{workspace_id}/clients",
            payload={"name": name},
        )

    @mcp.tool()
    def toggl_update_client(
        workspace_id: int, client_id: int, name: str
    ) -> str:
        """Update a client's name.

        Args:
            workspace_id: The workspace ID.
            client_id: The client ID.
            name: New client name.
        """
        return client.put(
            f"/api/v9/workspaces/{workspace_id}/clients/{client_id}",
            payload={"name": name},
        )

    @mcp.tool()
    def toggl_delete_client(workspace_id: int, client_id: int) -> str:
        """Delete a client.

        Args:
            workspace_id: The workspace ID.
            client_id: The client ID.
        """
        return client.delete(
            f"/api/v9/workspaces/{workspace_id}/clients/{client_id}"
        )

    @mcp.tool()
    def toggl_archive_client(workspace_id: int, client_id: int) -> str:
        """Archive a client.

        Args:
            workspace_id: The workspace ID.
            client_id: The client ID.
        """
        return client.post(
            f"/api/v9/workspaces/{workspace_id}/clients/{client_id}/archive"
        )

    @mcp.tool()
    def toggl_restore_client(workspace_id: int, client_id: int) -> str:
        """Restore an archived client.

        Args:
            workspace_id: The workspace ID.
            client_id: The client ID.
        """
        return client.post(
            f"/api/v9/workspaces/{workspace_id}/clients/{client_id}/restore"
        )
