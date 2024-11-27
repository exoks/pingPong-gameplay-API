from channels.generic.websocket import AsyncWebsocketConsumer
from .tasks import matchmaker, matchmaker_group
from .player_model import Player
import json


class PlayerConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_name = matchmaker_group
        await self.accept()
        print("[CONSUMER: ]: connection accepted")
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(f"[CONSUMER: ]: > data is recived {data}")
        self.player = Player(data['id'], data['rank'])
        matchmaker.delay(
            player_id=self.player.id,
            player_rank=self.player.rank,
        )

    async def match_found(self, event):
        if self.player.id in event['match']:
            print(f"[MATCH_FOUND]: > {event}")
            opponent_id = event['match'].replace(self.player.id, '')
            await self.send(text_data=json.dumps({
                "player_id": self.player.id,
                "opponent_id": opponent_id,
                "room_id": event['room_id'],
            }))
            print(f"[CONSUMER: ]: > Data sent to client <{self.player.id}>")
