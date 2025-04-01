import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from .tracking_module import update_driver_location, get_driver_location

class LocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.channel_layer = get_channel_layer()
        self.room_group_name = "driver_tracking"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            driver_id = data.get("driver_id")
            latitude = float(data.get("latitude"))
            longitude = float(data.get("longitude"))

            if not all([driver_id, latitude, longitude]):
                await self.send(json.dumps({"error": "Missing parameters"}))
                return

            update_driver_location(driver_id, latitude, longitude)

            # Broadcast location update to all connected clients
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "send_location_update",
                    "message": {
                        "driver_id": driver_id,
                        "latitude": latitude,
                        "longitude": longitude
                    }
                }
            )

        except json.JSONDecodeError:
            await self.send(json.dumps({"error": "Invalid JSON data"}))

    async def send_location_update(self, event):
        await self.send(json.dumps(event["message"]))