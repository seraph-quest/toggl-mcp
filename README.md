# Toggl Track MCP Server

MCP server for [Toggl Track](https://toggl.com/track/) time tracking, optimized for [Seraph](https://github.com/seraph-quest/seraph/) with support for Claude Desktop via stdio.

**40 tools** covering time entries, projects, clients, tags, tasks, reports, insights, and webhooks.

## Modes

| Mode | Tools | Description |
|------|-------|-------------|
| `read` (default) | 20 | Safe read-only access — queries, reports, insights |
| `readwrite` | 40 | Full CRUD — create/update/delete time entries, projects, etc. |

Write tools are **not registered** in read mode — the LLM never sees them.

## Quick Start

### Docker (recommended for Seraph)

```bash
cp .env.example .env
# Edit .env with your Toggl API key
docker compose up -d
```

### Local

```bash
uv sync
TOGGL_API_KEY=your_token uv run python server.py
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `TOGGL_API_KEY` | (required) | API token from [Toggl Profile](https://track.toggl.com/profile) |
| `TOGGL_MODE` | `read` | `read` or `readwrite` |
| `TRANSPORT` | `http` | `http` (streamable-http) or `stdio` |
| `PORT` | `9300` | HTTP port (http transport only) |

## Seraph Integration

Register via CLI:

```bash
./mcp.sh add toggl http://toggl-mcp:9300/mcp --desc "Toggl Track time tracking"
```

Or add to `mcp-servers.json`:

```json
{
  "toggl": {
    "url": "http://toggl-mcp:9300/mcp",
    "enabled": true,
    "description": "Toggl Track time tracking"
  }
}
```

## Claude Desktop Integration

Add to your Claude Desktop MCP config:

```json
{
  "mcpServers": {
    "toggl": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/toggle-mcp", "python", "server.py"],
      "env": {
        "TOGGL_API_KEY": "your_token",
        "TOGGL_MODE": "readwrite",
        "TRANSPORT": "stdio"
      }
    }
  }
}
```

## Tool Reference

### Read Tools (20)

| Tool | Description |
|------|-------------|
| `toggl_get_me` | Get authenticated user profile |
| `toggl_get_time_entries` | Get recent time entries |
| `toggl_get_current_timer` | Get running timer |
| `toggl_get_time_entry` | Get time entry by ID |
| `toggl_list_workspaces` | List workspaces |
| `toggl_get_workspace` | Get workspace details |
| `toggl_list_workspace_users` | List workspace users |
| `toggl_list_projects` | List workspace projects |
| `toggl_get_project` | Get project details |
| `toggl_list_clients` | List workspace clients |
| `toggl_get_client` | Get client details |
| `toggl_list_tags` | List workspace tags |
| `toggl_list_tasks` | List project tasks |
| `toggl_get_task` | Get task details |
| `toggl_list_webhooks` | List webhook subscriptions |
| `toggl_report_summary` | Summary report |
| `toggl_report_detailed` | Detailed report (paginated) |
| `toggl_report_weekly` | Weekly report |
| `toggl_project_data_trends` | Project data trends |
| `toggl_project_profitability` | Project profitability |

### Write Tools (20, readwrite mode only)

| Tool | Description |
|------|-------------|
| `toggl_create_time_entry` | Create time entry / start timer |
| `toggl_update_time_entry` | Update time entry |
| `toggl_delete_time_entry` | Delete time entry |
| `toggl_stop_timer` | Stop running timer |
| `toggl_create_project` | Create project |
| `toggl_update_project` | Update project |
| `toggl_delete_project` | Delete project |
| `toggl_create_client` | Create client |
| `toggl_update_client` | Update client |
| `toggl_delete_client` | Delete client |
| `toggl_archive_client` | Archive client |
| `toggl_restore_client` | Restore archived client |
| `toggl_create_tag` | Create tag |
| `toggl_update_tag` | Update tag |
| `toggl_delete_tag` | Delete tag |
| `toggl_create_task` | Create task (premium) |
| `toggl_update_task` | Update task (premium) |
| `toggl_delete_task` | Delete task (premium) |
| `toggl_create_webhook` | Create webhook subscription |
| `toggl_delete_webhook` | Delete webhook subscription |
