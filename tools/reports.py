"""Reports API tools (summary, detailed, weekly)."""

import json

from mcp.server.fastmcp import FastMCP

from toggl_client import TogglClient


def register_read(mcp: FastMCP, client: TogglClient) -> None:
    @mcp.tool()
    def toggl_report_summary(
        workspace_id: int,
        start_date: str,
        end_date: str,
        project_ids: list[int] | None = None,
        client_ids: list[int] | None = None,
        grouping: str | None = None,
        sub_grouping: str | None = None,
    ) -> str:
        """Get a summary report of time entries.

        Args:
            workspace_id: The workspace ID.
            start_date: Start date (YYYY-MM-DD).
            end_date: End date (YYYY-MM-DD).
            project_ids: Filter by project IDs.
            client_ids: Filter by client IDs.
            grouping: Group by: projects, clients, users, or time_entries.
            sub_grouping: Sub-group by: projects, clients, users, or time_entries.
        """
        payload: dict = {"start_date": start_date, "end_date": end_date}
        if project_ids:
            payload["project_ids"] = project_ids
        if client_ids:
            payload["client_ids"] = client_ids
        if grouping:
            payload["grouping"] = grouping
        if sub_grouping:
            payload["sub_grouping"] = sub_grouping
        return client.post(
            f"/reports/api/v3/workspace/{workspace_id}/summary/time_entries",
            payload=payload,
        )

    @mcp.tool()
    def toggl_report_detailed(
        workspace_id: int,
        start_date: str,
        end_date: str,
        project_ids: list[int] | None = None,
        client_ids: list[int] | None = None,
        first_row_number: int | None = None,
    ) -> str:
        """Get a detailed report of time entries (paginated).

        Args:
            workspace_id: The workspace ID.
            start_date: Start date (YYYY-MM-DD).
            end_date: End date (YYYY-MM-DD).
            project_ids: Filter by project IDs.
            client_ids: Filter by client IDs.
            first_row_number: Pagination offset (1-based). Omit for first page.
        """
        payload: dict = {"start_date": start_date, "end_date": end_date}
        if project_ids:
            payload["project_ids"] = project_ids
        if client_ids:
            payload["client_ids"] = client_ids
        if first_row_number is not None:
            payload["first_row_number"] = first_row_number
        return client.post(
            f"/reports/api/v3/workspace/{workspace_id}/search/time_entries",
            payload=payload,
        )

    @mcp.tool()
    def toggl_report_weekly(
        workspace_id: int,
        start_date: str,
        end_date: str,
        project_ids: list[int] | None = None,
        client_ids: list[int] | None = None,
        grouping: str | None = None,
    ) -> str:
        """Get a weekly report of time entries.

        Args:
            workspace_id: The workspace ID.
            start_date: Start date (YYYY-MM-DD).
            end_date: End date (YYYY-MM-DD).
            project_ids: Filter by project IDs.
            client_ids: Filter by client IDs.
            grouping: Group by: projects, clients, or users.
        """
        payload: dict = {"start_date": start_date, "end_date": end_date}
        if project_ids:
            payload["project_ids"] = project_ids
        if client_ids:
            payload["client_ids"] = client_ids
        if grouping:
            payload["grouping"] = grouping
        return client.post(
            f"/reports/api/v3/workspace/{workspace_id}/weekly/time_entries",
            payload=payload,
        )


def register_write(mcp: FastMCP, client: TogglClient) -> None:
    pass  # Reports are read-only
