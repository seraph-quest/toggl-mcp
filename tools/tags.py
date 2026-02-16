"""Tag read + write tools."""

from mcp.server.fastmcp import FastMCP

from toggl_client import TogglClient


def register_read(mcp: FastMCP, client: TogglClient) -> None:
    @mcp.tool()
    def toggl_list_tags(workspace_id: int) -> str:
        """List all tags in a workspace.

        Args:
            workspace_id: The workspace ID.
        """
        return client.get(f"/api/v9/workspaces/{workspace_id}/tags")


def register_write(mcp: FastMCP, client: TogglClient) -> None:
    @mcp.tool()
    def toggl_create_tag(workspace_id: int, name: str) -> str:
        """Create a new tag in a workspace.

        Args:
            workspace_id: The workspace ID.
            name: Tag name.
        """
        return client.post(
            f"/api/v9/workspaces/{workspace_id}/tags",
            payload={"name": name},
        )

    @mcp.tool()
    def toggl_update_tag(workspace_id: int, tag_id: int, name: str) -> str:
        """Rename a tag.

        Args:
            workspace_id: The workspace ID.
            tag_id: The tag ID.
            name: New tag name.
        """
        return client.put(
            f"/api/v9/workspaces/{workspace_id}/tags/{tag_id}",
            payload={"name": name},
        )

    @mcp.tool()
    def toggl_delete_tag(workspace_id: int, tag_id: int) -> str:
        """Delete a tag.

        Args:
            workspace_id: The workspace ID.
            tag_id: The tag ID.
        """
        return client.delete(
            f"/api/v9/workspaces/{workspace_id}/tags/{tag_id}"
        )
