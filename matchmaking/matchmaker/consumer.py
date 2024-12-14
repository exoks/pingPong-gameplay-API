#  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣦⣴⣶⣾⣿⣶⣶⣶⣶⣦⣤⣄⠀⠀⠀⠀⠀⠀⠀
#  ⠀⠀⠀⠀⠀⠀⠀⢠⡶⠻⠛⠟⠋⠉⠀⠈⠤⠴⠶⠶⢾⣿⣿⣿⣷⣦⠄⠀⠀⠀             𓐓  consumer.py 𓐔           
#  ⠀⠀⠀⠀⠀⢀⠔⠋⠀⠀⠤⠒⠒⢲⠀⠀⠀⢀⣠⣤⣤⣬⣽⣿⣿⣿⣷⣄⠀⠀
#  ⠀⠀⠀⣀⣎⢤⣶⣾⠅⠀⠀⢀⡤⠏⠀⠀⠀⠠⣄⣈⡙⠻⢿⣿⣿⣿⣿⣿⣦⠀   Student: oezzaou <oezzaou@student.1337.ma>
#  ⢀⠔⠉⠀⠊⠿⠿⣿⠂⠠⠢⣤⠤⣤⣼⣿⣶⣶⣤⣝⣻⣷⣦⣍⡻⣿⣿⣿⣿⡀
#  ⢾⣾⣆⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠉⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
#  ⠀⠈⢋⢹⠋⠉⠙⢦⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇       Created: 2024/12/06 09:33:14 by oezzaou
#  ⠀⠀⠀⠑⠀⠀⠀⠈⡇⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇       Updated: 2024/12/13 23:50:54 by oezzaou
#  ⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⢀⣾⣿⣿⠿⠟⠛⠋⠛⢿⣿⣿⠻⣿⣿⣿⣿⡿⠀
#  ⠀⠀⠀⠀⠀⠀⠀⢀⠇⠀⢠⣿⣟⣭⣤⣶⣦⣄⡀⠀⠀⠈⠻⠀⠘⣿⣿⣿⠇⠀
#  ⠀⠀⠀⠀⠀⠱⠤⠊⠀⢀⣿⡿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠘⣿⠏⠀⠀                             𓆩♕𓆪
#  ⠀⠀⠀⠀⠀⡄⠀⠀⠀⠘⢧⡀⠀⠀⠸⣿⣿⣿⠟⠀⠀⠀⠀⠀⠀⠐⠋⠀⠀⠀                     𓄂 oussama ezzaou𓆃
#  ⠀⠀⠀⠀⠀⠘⠄⣀⡀⠸⠓⠀⠀⠀⠠⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

# ====<[ Modules: ]>===========================================================
from channels.generic.websocket import AsyncWebsocketConsumer
from .tasks import matchmaker
import json
import redis


class PlayerConsumer(AsyncWebsocketConsumer):

    # ====<[ connect: websocket connection established ]>======================
    async def connect(self):
        # WARNING: > PLAYER_ID must be taken form webtoken
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.player_cache = f"{self.room_id}_cache"
        await self.channel_layer.group_add(self.room_id, self.channel_name)
        await self.accept()
        print("[CONSUMER: ]: connection accepted")

    # ====<[ disconnect: when consumer disconnected ]>=========================
    async def disconnect(self, code):
        redis_conn = redis.StrictRedis(host='redis', port=6379)
        redis_conn.zrem(self.player_cache, self.player_id)
        await self.channel_layer.group_discard(self.room_id, self.channel_name)
        redis_conn.close()

    # ====<[ receive: receive data from client-side ]>=========================
    async def receive(self, text_data):
        data = json.loads(text_data)
        self.player_id = data['id']  # NOTE: > must be taken from webtoken
        self.player_rank = data['rank']
        matchmaker.delay(self.room_id,
                         self.player_cache,
                         self.player_id,
                         self.player_rank)
        print(f"[CONSUMER: ]: > data is recived {data}")

    # ====<[ match_found: send match players to client side ]>=================
    async def match_found(self, event):
        if self.player_id in event['match']:
            opponent_id = event['match'].replace(self.player_id, '')
            await self.send(text_data=json.dumps({
                "player_id": self.player_id,
                "opponent_id": opponent_id,
                "room_id": event['room_id'],
            }))
            print(f"[MATCH_FOUND]: > {event}")
            print(f"[CONSUMER: ]: > Data sent to client <{self.player_id}>")
