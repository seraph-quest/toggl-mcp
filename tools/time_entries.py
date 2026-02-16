"""Time entry write tools."""

from mcp.server.fastmcp import FastMCP

from toggl_client import TogglClient


def register_read(mcp: FastMCP, client: TogglClient) -> None:
    pass  # Read tools are in me.py


def register_write(mcp: FastMCP, client: TogglClient) -> None:
    @mcp.tool()
    def toggl_create_time_entry(
        workspace_id: int,
        description: str | None = None,
        project_id: int | None = None,
        start: str | None = None,
        duration: int = -1,
        tags: list[str] | None = None,
        created_with: str = "toggl-mcp",
    ) -> str:
        """Create a time entry. Set duration=-1 to start a running timer.

        Args:
            workspace_id: The workspace ID.
            description: Time entry description.
            project_id: Project ID to assign.
            start: Start time in ISO 8601 (e.g. 2024-01-01T09:00:00Z). Defaults to now.
            duration: Duration in seconds. Use -1 to start a running timer (default).
            tags: List of tag names.
            created_with: App identifier. Defaults to "toggl-mcp".
        """
        payload: dict = {
            "workspace_id": workspace_id,
            "duration": duration,
            "created_with": created_with,
        }
        if description is not None:
            payload["description"] = description
        if project_id is not None:
            payload["project_id"] = project_id
        if start is not None:
            payload["start"] = start
        if tags:
            payload["tags"] = tags
        return client.post(
            f"/api/v9/workspaces/{workspace_id}/time_entries",
            payload=payload,
        )

    @mcp.tool()
    def toggl_update_time_entry(
        workspace_id: int,
        time_entry_id: int,
        description: str | None = None,
        project_id: int | None = None,
        start: str | None = None,
        stop: str | None = None,
        duration: int | None = None,
        tags: list[str] | None = None,
    ) -> str:
        """Update an existing time entry.

        Args:
            workspace_id: The workspace ID.
            time_entry_id: The time entry ID.
            description: New description.
            project_id: New project ID.
            start: New start time (ISO 8601).
            stop: New stop time (ISO 8601).
            duration: New duration in seconds.
            tags: New list of tag names (replaces existing).
        """
        payload: dict = {}
        if description is not None:
            payload["description"] = description
        if project_id is not None:
            payload["project_id"] = project_id
        if start is not None:
            payload["start"] = start
        if stop is not None:
            payload["stop"] = stop
        if duration is not None:
            payload["duration"] = duration
        if tags is not None:
            payload["tags"] = tags
        return client.put(
            f"/api/v9/workspaces/{workspace_id}/time_entries/{time_entry_id}",
            payload=payload,
        )

    @mcp.tool()
    def toggl_delete_time_entry(
        workspace_id: int, time_entry_id: int
    ) -> str:
        """Delete a time entry.

        Args:
            workspace_id: The workspace ID.
            time_entry_id: The time entry ID.
        """
        return client.delete(
            f"/api/v9/workspaces/{workspace_id}/time_entries/{time_entry_id}"
        )

    @mcp.tool()
    def toggl_stop_timer(workspace_id: int, time_entry_id: int) -> str:
        """Stop a running timer.

        Args:
            workspace_id: The workspace ID.
            time_entry_id: The running time entry ID.
        """
        return client.patch(
            f"/api/v9/workspaces/{workspace_id}/time_entries/{time_entry_id}/stop"
        )
