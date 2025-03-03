#  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣦⣴⣶⣾⣿⣶⣶⣶⣶⣦⣤⣄⠀⠀⠀⠀⠀⠀⠀
#  ⠀⠀⠀⠀⠀⠀⠀⢠⡶⠻⠛⠟⠋⠉⠀⠈⠤⠴⠶⠶⢾⣿⣿⣿⣷⣦⠄⠀⠀⠀            𓐓  consumers.py 𓐔
#  ⠀⠀⠀⠀⠀⢀⠔⠋⠀⠀⠤⠒⠒⢲⠀⠀⠀⢀⣠⣤⣤⣬⣽⣿⣿⣿⣷⣄⠀⠀
#  ⠀⠀⠀⣀⣎⢤⣶⣾⠅⠀⠀⢀⡤⠏⠀⠀⠀⠠⣄⣈⡙⠻⢿⣿⣿⣿⣿⣿⣦⠀   Student: oezzaou <oezzaou@student.1337.ma>
#  ⢀⠔⠉⠀⠊⠿⠿⣿⠂⠠⠢⣤⠤⣤⣼⣿⣶⣶⣤⣝⣻⣷⣦⣍⡻⣿⣿⣿⣿⡀
#  ⢾⣾⣆⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠉⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
#  ⠀⠈⢋⢹⠋⠉⠙⢦⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇       Created: 2024/11/24 10:50:16 by oezzaou
#  ⠀⠀⠀⠑⠀⠀⠀⠈⡇⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇       Updated: 2024/12/14 03:28:17 by oezzaou
#  ⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⢀⣾⣿⣿⠿⠟⠛⠋⠛⢿⣿⣿⠻⣿⣿⣿⣿⡿⠀
#  ⠀⠀⠀⠀⠀⠀⠀⢀⠇⠀⢠⣿⣟⣭⣤⣶⣦⣄⡀⠀⠀⠈⠻⠀⠘⣿⣿⣿⠇⠀
#  ⠀⠀⠀⠀⠀⠱⠤⠊⠀⢀⣿⡿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠘⣿⠏⠀⠀                             𓆩♕𓆪
#  ⠀⠀⠀⠀⠀⡄⠀⠀⠀⠘⢧⡀⠀⠀⠸⣿⣿⣿⠟⠀⠀⠀⠀⠀⠀⠐⠋⠀⠀⠀                     𓄂 oussama ezzaou𓆃
#  ⠀⠀⠀⠀⠀⠘⠄⣀⡀⠸⠓⠀⠀⠀⠠⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

# ====<[ Modules: ]>===========================================================
from channels.generic.websocket import AsyncWebsocketConsumer
from .tasks import start_gameplay
import json
import random
import redis


class PlayerConsumer(AsyncWebsocketConsumer):

    # =====<[ connect: establish websocket connection: ]>======================
    async def connect(self):
        headers = dict(self.scope['headers'])
        x_user_id = headers.get(b'x-user-id', None)
        if x_user_id is None:
            await self.close()
        self.player_id = x_user_id.decode('utf-8')
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.redis_conn = redis.StrictRedis(host="redis", port=6379)
        self.game_cache = f"{self.room_id}_cache"
        self.player_state = f"{self.player_id}_state"
        self.redis_conn.hset(self.game_cache, self.player_state, "available")
        self.initiator = False
        await self.channel_layer.group_add(self.room_id, self.channel_name)
        await self.channel_layer.group_send(self.room_id, {
            "type": "join_lobby",
            "opponent_id": self.player_id,
        })
        await self.accept()
        print(f"[SERVER: CONNECT]: > id:{self.player_id}, room:{self.room_id}")

    # ====<[ disconnect: when connection closed ]>=============================
    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_id, self.channel_name)
        # self.redis_conn.delete(self.game_cache)
        self.redis_conn.hset(self.game_cache, self.player_state, "unavailable")
        self.redis_conn.close()
        print("[SERVER: DISCONNECT]: > connection closed")

    # ====<[ receive: receive data from client-side ]>=========================
    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(self.room_id, {
            "type": "paddle_state",
            "player_id": self.player_id,
            "paddle_y": data['paddle_y'],
        })
        paddle_y = f"{self.player_id}_paddle_y"
        self.redis_conn.hset(self.game_cache, paddle_y, data['paddle_y'])

    # ====<[ join_lobby: gather players in lobby to start game ]>==============
    async def join_lobby(self, text_data):
        opponent_id = text_data['opponent_id']
        if self.player_id != opponent_id:
            self.initiator = True
            start_gameplay.delay(self.player_id,
                                 opponent_id,
                                 self.room_id,
                                 self.game_cache)
            print("[SERVER: MESSAGE: > starting game")

    # ====<[ gameplay_init: initiate the game for client-side ]>===============
    async def gameplay_init(self, game_data):
        player, opponent = (0, 1) if self.initiator is True else (1, 0)
        await self.send(json.dumps({
            "event": game_data['type'],
            "ball": game_data['ball'],
            "paddle_x": game_data['paddle_x'][player],
            "player_score": game_data['score'][player],
            "opponent_score": game_data['score'][opponent],
        }))

# ====<[ paddle_state: update paddle_state in client-side ]>===================
    async def paddle_state(self, data):
        if self.player_id != data['player_id']:
            await self.send(json.dumps({
                "event": data['type'],
                "paddle_y": data['paddle_y'],
            }))
        # print(f"[SERVER: EVENT] > paddle state <{data}>")

    # ====<[ ball_state: update ball state in client-sdie ]>===================
    async def ball_state(self, ball_data):
        await self.send(json.dumps({
            "event": ball_data['type'],
            "ball": ball_data['ball'],
        }))

    # ====<[ gameplay_state: update game state in client-sdie ]>===============
    async def gameplay_reinit(self, game_data):
        player, opponent = (0, 1) if self.initiator is True else (1, 0)
        await self.send(json.dumps({
            "event": game_data['type'],
            "ball": game_data['ball'],
            "paddle_x": game_data['paddle_x'][player],
            "player_score": game_data['score'][player],
            "opponent_score": game_data['score'][opponent],
        }))
        # self.redis_conn.delete(self.game_cache)

    # ====<[ gameplay_stop: stop the game play ]>==============================
    async def gameplay_stop(self, game_data):
        if self.player_id != game_data['player_id']:
            await self.send(json.dumps({
                "event": game_data['type'],
                "timer": game_data['timer']
            }))

    # ====<[ gameplay_end: end game in client-side ]>==========================
    async def gameplay_end(self, game_data):
        await self.send(json.dumps({
            "event": game_data['type'],
            "winner_id": game_data['winner_id'],
            "loser_id": game_data['loser_id'],
            "winner_score": game_data['winner_score'],
            "loser_score": game_data['loser_score'],
        }))

        # type: "gameplay_end", winner_id: "bjdaarcemf", loser_id: "jdmnfrdhqd", winner_score: 6, loser_score: 0
