"""Tool registration orchestrator."""

from mcp.server.fastmcp import FastMCP

from toggl_client import TogglClient

from tools import (
    clients,
    insights,
    me,
    projects,
    reports,
    tags,
    tasks,
    time_entries,
    webhooks,
    workspaces,
)

READ_MODULES = [me, workspaces, projects, clients, tags, tasks, reports, insights, webhooks]
WRITE_MODULES = [time_entries, projects, clients, tags, tasks, webhooks]


def register_read_tools(mcp: FastMCP, client: TogglClient) -> None:
    for mod in READ_MODULES:
        mod.register_read(mcp, client)


def register_write_tools(mcp: FastMCP, client: TogglClient) -> None:
    for mod in WRITE_MODULES:
        mod.register_write(mcp, client)
