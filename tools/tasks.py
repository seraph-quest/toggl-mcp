"""Task read + write tools (premium feature)."""

from mcp.server.fastmcp import FastMCP

from toggl_client import TogglClient


def register_read(mcp: FastMCP, client: TogglClient) -> None:
    @mcp.tool()
    def toggl_list_tasks(workspace_id: int, project_id: int) -> str:
        """List tasks for a project (requires premium).

        Args:
            workspace_id: The workspace ID.
            project_id: The project ID.
        """
        return client.get(
            f"/api/v9/workspaces/{workspace_id}/projects/{project_id}/tasks"
        )

    @mcp.tool()
    def toggl_get_task(workspace_id: int, project_id: int, task_id: int) -> str:
        """Get a specific task (requires premium).

        Args:
            workspace_id: The workspace ID.
            project_id: The project ID.
            task_id: The task ID.
        """
        return client.get(
            f"/api/v9/workspaces/{workspace_id}/projects/{project_id}/tasks/{task_id}"
        )


def register_write(mcp: FastMCP, client: TogglClient) -> None:
    @mcp.tool()
    def toggl_create_task(
        workspace_id: int,
        project_id: int,
        name: str,
        estimated_seconds: int | None = None,
    ) -> str:
        """Create a task in a project (requires premium).

        Args:
            workspace_id: The workspace ID.
            project_id: The project ID.
            name: Task name.
            estimated_seconds: Estimated duration in seconds.
        """
        payload: dict = {"name": name}
        if estimated_seconds is not None:
            payload["estimated_seconds"] = estimated_seconds
        return client.post(
            f"/api/v9/workspaces/{workspace_id}/projects/{project_id}/tasks",
            payload=payload,
        )

    @mcp.tool()
    def toggl_update_task(
        workspace_id: int,
        project_id: int,
        task_id: int,
        name: str | None = None,
        estimated_seconds: int | None = None,
        active: bool | None = None,
    ) -> str:
        """Update a task (requires premium).

        Args:
            workspace_id: The workspace ID.
            project_id: The project ID.
            task_id: The task ID.
            name: New task name.
            estimated_seconds: New estimated duration in seconds.
            active: New active status.
        """
        payload: dict = {}
        if name is not None:
            payload["name"] = name
        if estimated_seconds is not None:
            payload["estimated_seconds"] = estimated_seconds
        if active is not None:
            payload["active"] = active
        return client.put(
            f"/api/v9/workspaces/{workspace_id}/projects/{project_id}/tasks/{task_id}",
            payload=payload,
        )

    @mcp.tool()
    def toggl_delete_task(
        workspace_id: int, project_id: int, task_id: int
    ) -> str:
        """Delete a task (requires premium).

        Args:
            workspace_id: The workspace ID.
            project_id: The project ID.
            task_id: The task ID.
        """
        return client.delete(
            f"/api/v9/workspaces/{workspace_id}/projects/{project_id}/tasks/{task_id}"
        )
