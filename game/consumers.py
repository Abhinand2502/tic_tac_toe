import json
from channels.generic.websocket import AsyncWebsocketConsumer

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "tic_tac_toe"
        self.room_group_name = f"game_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Assign player when they join (first X, second O)
        if not hasattr(self.channel_layer, "players"):
            self.channel_layer.players = []
        
        if self.channel_name not in self.channel_layer.players:
            if len(self.channel_layer.players) == 0:
                self.player = "X"
            else:
                self.player = "O"
            self.channel_layer.players.append(self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        if hasattr(self.channel_layer, "players") and self.channel_name in self.channel_layer.players:
            self.channel_layer.players.remove(self.channel_name)

    async def receive(self, text_data):   # <-- FIX: moved inside class
        data = json.loads(text_data)

        # Only handle moves
        if "row" in data and "col" in data:
            row = data["row"]
            col = data["col"]

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "game_move",
                    "row": row,
                    "col": col,
                    "player": self.player
                }
            )
        else:
            # Optional: log or ignore system messages
            print("Non-move message received:", data)

    async def game_move(self, event):
        await self.send(text_data=json.dumps({
            "row": event["row"],
            "col": event["col"],
            "player": event["player"]
        }))
