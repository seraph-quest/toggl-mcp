"""Project read + write tools."""

from mcp.server.fastmcp import FastMCP

from toggl_client import TogglClient


def register_read(mcp: FastMCP, client: TogglClient) -> None:
    @mcp.tool()
    def toggl_list_projects(
        workspace_id: int,
        active: bool | None = None,
    ) -> str:
        """List projects in a workspace.

        Args:
            workspace_id: The workspace ID.
            active: Filter by active status. Omit to return all.
        """
        params = {}
        if active is not None:
            params["active"] = str(active).lower()
        return client.get(
            f"/api/v9/workspaces/{workspace_id}/projects",
            params=params or None,
        )

    @mcp.tool()
    def toggl_get_project(workspace_id: int, project_id: int) -> str:
        """Get a specific project.

        Args:
            workspace_id: The workspace ID.
            project_id: The project ID.
        """
        return client.get(
            f"/api/v9/workspaces/{workspace_id}/projects/{project_id}"
        )


def register_write(mcp: FastMCP, client: TogglClient) -> None:
    @mcp.tool()
    def toggl_create_project(
        workspace_id: int,
        name: str,
        client_id: int | None = None,
        is_private: bool = True,
        active: bool = True,
        color: str | None = None,
    ) -> str:
        """Create a new project in a workspace.

        Args:
            workspace_id: The workspace ID.
            name: Project name.
            client_id: Optional client ID to assign.
            is_private: Whether the project is private. Defaults to True.
            active: Whether the project is active. Defaults to True.
            color: Hex color code (e.g. "#ff0000").
        """
        payload: dict = {"name": name, "is_private": is_private, "active": active}
        if client_id is not None:
            payload["client_id"] = client_id
        if color is not None:
            payload["color"] = color
        return client.post(
            f"/api/v9/workspaces/{workspace_id}/projects", payload=payload
        )

    @mcp.tool()
    def toggl_update_project(
        workspace_id: int,
        project_id: int,
        name: str | None = None,
        client_id: int | None = None,
        is_private: bool | None = None,
        active: bool | None = None,
        color: str | None = None,
    ) -> str:
        """Update an existing project.

        Args:
            workspace_id: The workspace ID.
            project_id: The project ID.
            name: New project name.
            client_id: New client ID.
            is_private: New privacy setting.
            active: New active status.
            color: New hex color code.
        """
        payload: dict = {}
        if name is not None:
            payload["name"] = name
        if client_id is not None:
            payload["client_id"] = client_id
        if is_private is not None:
            payload["is_private"] = is_private
        if active is not None:
            payload["active"] = active
        if color is not None:
            payload["color"] = color
        return client.put(
            f"/api/v9/workspaces/{workspace_id}/projects/{project_id}",
            payload=payload,
        )

    @mcp.tool()
    def toggl_delete_project(workspace_id: int, project_id: int) -> str:
        """Delete a project.

        Args:
            workspace_id: The workspace ID.
            project_id: The project ID.
        """
        return client.delete(
            f"/api/v9/workspaces/{workspace_id}/projects/{project_id}"
        )
