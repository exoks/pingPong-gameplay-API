#  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣦⣴⣶⣾⣿⣶⣶⣶⣶⣦⣤⣄⠀⠀⠀⠀⠀⠀⠀
#  ⠀⠀⠀⠀⠀⠀⠀⢠⡶⠻⠛⠟⠋⠉⠀⠈⠤⠴⠶⠶⢾⣿⣿⣿⣷⣦⠄⠀⠀⠀            𓐓  consumers.py 𓐔           
#  ⠀⠀⠀⠀⠀⢀⠔⠋⠀⠀⠤⠒⠒⢲⠀⠀⠀⢀⣠⣤⣤⣬⣽⣿⣿⣿⣷⣄⠀⠀
#  ⠀⠀⠀⣀⣎⢤⣶⣾⠅⠀⠀⢀⡤⠏⠀⠀⠀⠠⣄⣈⡙⠻⢿⣿⣿⣿⣿⣿⣦⠀   Student: oezzaou <oezzaou@student.1337.ma>
#  ⢀⠔⠉⠀⠊⠿⠿⣿⠂⠠⠢⣤⠤⣤⣼⣿⣶⣶⣤⣝⣻⣷⣦⣍⡻⣿⣿⣿⣿⡀
#  ⢾⣾⣆⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠉⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
#  ⠀⠈⢋⢹⠋⠉⠙⢦⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇       Created: 2024/11/24 10:50:16 by oezzaou
#  ⠀⠀⠀⠑⠀⠀⠀⠈⡇⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇       Updated: 2024/11/27 21:41:11 by oezzaou
#  ⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⢀⣾⣿⣿⠿⠟⠛⠋⠛⢿⣿⣿⠻⣿⣿⣿⣿⡿⠀
#  ⠀⠀⠀⠀⠀⠀⠀⢀⠇⠀⢠⣿⣟⣭⣤⣶⣦⣄⡀⠀⠀⠈⠻⠀⠘⣿⣿⣿⠇⠀
#  ⠀⠀⠀⠀⠀⠱⠤⠊⠀⢀⣿⡿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠘⣿⠏⠀⠀                             𓆩♕𓆪
#  ⠀⠀⠀⠀⠀⡄⠀⠀⠀⠘⢧⡀⠀⠀⠸⣿⣿⣿⠟⠀⠀⠀⠀⠀⠀⠐⠋⠀⠀⠀                     𓄂 oussama ezzaou𓆃
#  ⠀⠀⠀⠀⠀⠘⠄⣀⡀⠸⠓⠀⠀⠀⠠⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

# ==== [ Modules: >============================================================
from channels.generic.websocket import AsyncWebsocketConsumer
from .tasks import start_gameplay
import json
import random
import redis

# ==== [ Global: >=============================================================
r = redis.StrictRedis(host="redis", port=6379, db=0)


class PlayerConsumer(AsyncWebsocketConsumer):

    # ====[ connect: establish websocket connection: >=========================
    async def connect(self):
        self.player_id = ''.join(random.choices("abcdefghijklmnopqrs", k=10))
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.game_event_queue = f"{self.room_id}_queue"
        # print(f" ==>> room_id: {self.room_id}")
        # print(f" ==>> player_id: {self.player_id}")

        await self.channel_layer.group_add(self.room_id, self.channel_name)
        await self.channel_layer.group_send(self.room_id, {
            "type": "join_lobby",
            "opponent_id": self.player_id,
        })
        await self.accept()
        print("[SERVER: CONNECTION]: > connection accepted")

    # ====[ disconnect: when connection closed >===============================
    async def disconnect(self, code):
        print("[SERVER: DISCONNECT]: > connection closed")
        await self.channel_layer.group_discard(self.room_id, self.channel_name)

    # ====[ receive: receive data from client-side >===========================
    async def receive(self, text_data):
        data = json.loads(text_data)
        self.player_id = data['player_id']
        # print(f"[SERVER: RECEIVE]: <{data}> data is received")
        # r.rpush(self.game_event_queue, json.dumps({
        #   self.player_id: data['paddle_y'],
        # }))

    # ====[ join_lobby: gather players in lobby to start game >================
    async def join_lobby(self, text_data):
        if (self.player_id != text_data['opponent_id']):
            print("[SERVER: MESSAGE]: > starting game")
            start_gameplay.delay(self.player_id, text_data['opponent_id'],
                                 self.room_id, self.game_event_queue)

    # ====[ gameplay_init: initiate the game for client-side >=================
    async def gameplay_init(self, init_state_data):
        player_data = init_state_data[self.player_id]
        await self.send(json.dumps({
            "event": init_state_data['type'],
            "ball": init_state_data['ball'],
            "paddle_x": player_data['paddle_x'],
            "player_score": player_data['player_score'],
            "opponent_score": player_data['opponent_score']
        }))

    # ====[ paddle_state: update paddle_state in client-side >=================
    async def paddle_state(self, paddle_data):
        print(f"[SERVER: EVENT] > paddle state <{paddle_data}>")
        if self.player_id not in paddle_data:
            await self.send(json.dumps(paddle_data))

    # ====[ ball_state: update ball state in client-sdie >=====================
    async def ball_state(self, ball_data):
        pass

    # ====[ gameplay_state: update game state in client-sdie >=================
    async def gameplay_reinitialize(self, reinit_state_data):
        await self.send(json.dumps(reinit_state_data))
