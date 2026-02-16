"""User profile and time entry read tools."""

from mcp.server.fastmcp import FastMCP

from toggl_client import TogglClient


def register_read(mcp: FastMCP, client: TogglClient) -> None:
    @mcp.tool()
    def toggl_get_me() -> str:
        """Get the authenticated user's profile including default workspace ID."""
        return client.get("/api/v9/me")

    @mcp.tool()
    def toggl_get_time_entries(
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> str:
        """Get time entries for the authenticated user.

        Args:
            start_date: ISO 8601 date (e.g. 2024-01-01). Defaults to ~9 days ago.
            end_date: ISO 8601 date. Defaults to now.
        """
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        return client.get("/api/v9/me/time_entries", params=params or None)

    @mcp.tool()
    def toggl_get_current_timer() -> str:
        """Get the currently running time entry, or null if no timer is running."""
        return client.get("/api/v9/me/time_entries/current")

    @mcp.tool()
    def toggl_get_time_entry(time_entry_id: int) -> str:
        """Get a specific time entry by ID.

        Args:
            time_entry_id: The time entry ID.
        """
        return client.get(f"/api/v9/me/time_entries/{time_entry_id}")


def register_write(mcp: FastMCP, client: TogglClient) -> None:
    pass  # No write tools in this module
