"""Insights API tools (trends, profitability)."""

from mcp.server.fastmcp import FastMCP

from toggl_client import TogglClient


def register_read(mcp: FastMCP, client: TogglClient) -> None:
    @mcp.tool()
    def toggl_project_data_trends(
        workspace_id: int,
        start_date: str,
        end_date: str,
        project_ids: list[int] | None = None,
    ) -> str:
        """Get project data trends (time tracked over periods).

        Args:
            workspace_id: The workspace ID.
            start_date: Start date (YYYY-MM-DD).
            end_date: End date (YYYY-MM-DD).
            project_ids: Filter by project IDs. Omit for all projects.
        """
        payload: dict = {"start_date": start_date, "end_date": end_date}
        if project_ids:
            payload["project_ids"] = project_ids
        return client.post(
            f"/insights/api/v1/workspace/{workspace_id}/data_trends/projects",
            payload=payload,
        )

    @mcp.tool()
    def toggl_project_profitability(
        workspace_id: int,
        start_date: str,
        end_date: str,
        project_ids: list[int] | None = None,
    ) -> str:
        """Get project profitability data (requires premium).

        Args:
            workspace_id: The workspace ID.
            start_date: Start date (YYYY-MM-DD).
            end_date: End date (YYYY-MM-DD).
            project_ids: Filter by project IDs. Omit for all projects.
        """
        payload: dict = {"start_date": start_date, "end_date": end_date}
        if project_ids:
            payload["project_ids"] = project_ids
        return client.post(
            f"/insights/api/v1/workspace/{workspace_id}/profitability/projects",
            payload=payload,
        )


def register_write(mcp: FastMCP, client: TogglClient) -> None:
    pass  # Insights are read-only
