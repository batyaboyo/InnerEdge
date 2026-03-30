"""WebSocket consumer for user alert stream."""

from __future__ import annotations

from channels.generic.websocket import AsyncJsonWebsocketConsumer


class AlertConsumer(AsyncJsonWebsocketConsumer):
    """Push alert notifications to authenticated users."""

    async def connect(self) -> None:
        user = self.scope.get("user")
        if not user or user.is_anonymous:
            await self.close()
            return
        self.group_name = f"alerts_{user.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code: int) -> None:
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def alert_message(self, event: dict) -> None:
        await self.send_json(event["payload"])
