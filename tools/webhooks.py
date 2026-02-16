"""Webhook read + write tools."""

from mcp.server.fastmcp import FastMCP

from toggl_client import TogglClient


def register_read(mcp: FastMCP, client: TogglClient) -> None:
    @mcp.tool()
    def toggl_list_webhooks(workspace_id: int) -> str:
        """List webhook subscriptions for a workspace.

        Args:
            workspace_id: The workspace ID.
        """
        return client.get(
            f"/webhooks/api/v1/subscriptions/{workspace_id}"
        )


def register_write(mcp: FastMCP, client: TogglClient) -> None:
    @mcp.tool()
    def toggl_create_webhook(
        workspace_id: int,
        url_callback: str,
        event_filters: list[str],
        enabled: bool = True,
        description: str | None = None,
    ) -> str:
        """Create a webhook subscription.

        Args:
            workspace_id: The workspace ID.
            url_callback: URL to receive webhook events.
            event_filters: Event types to subscribe to (e.g. ["time_entry.created"]).
            enabled: Whether the webhook is enabled. Defaults to True.
            description: Optional description.
        """
        payload: dict = {
            "url_callback": url_callback,
            "event_filters": event_filters,
            "enabled": enabled,
        }
        if description is not None:
            payload["description"] = description
        return client.post(
            f"/webhooks/api/v1/subscriptions/{workspace_id}",
            payload=payload,
        )

    @mcp.tool()
    def toggl_delete_webhook(
        workspace_id: int, subscription_id: int
    ) -> str:
        """Delete a webhook subscription.

        Args:
            workspace_id: The workspace ID.
            subscription_id: The webhook subscription ID.
        """
        return client.delete(
            f"/webhooks/api/v1/subscriptions/{workspace_id}/{subscription_id}"
        )
