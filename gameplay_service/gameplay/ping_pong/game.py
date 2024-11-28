#  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣦⣴⣶⣾⣿⣶⣶⣶⣶⣦⣤⣄⠀⠀⠀⠀⠀⠀⠀
#  ⠀⠀⠀⠀⠀⠀⠀⢠⡶⠻⠛⠟⠋⠉⠀⠈⠤⠴⠶⠶⢾⣿⣿⣿⣷⣦⠄⠀⠀⠀                 𓐓  game.py 𓐔           
#  ⠀⠀⠀⠀⠀⢀⠔⠋⠀⠀⠤⠒⠒⢲⠀⠀⠀⢀⣠⣤⣤⣬⣽⣿⣿⣿⣷⣄⠀⠀
#  ⠀⠀⠀⣀⣎⢤⣶⣾⠅⠀⠀⢀⡤⠏⠀⠀⠀⠠⣄⣈⡙⠻⢿⣿⣿⣿⣿⣿⣦⠀   Student: oezzaou <oezzaou@student.1337.ma>
#  ⢀⠔⠉⠀⠊⠿⠿⣿⠂⠠⠢⣤⠤⣤⣼⣿⣶⣶⣤⣝⣻⣷⣦⣍⡻⣿⣿⣿⣿⡀
#  ⢾⣾⣆⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠉⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
#  ⠀⠈⢋⢹⠋⠉⠙⢦⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇       Created: 2024/11/24 07:24:58 by oezzaou
#  ⠀⠀⠀⠑⠀⠀⠀⠈⡇⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇       Updated: 2024/11/28 16:32:17 by oezzaou
#  ⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⢀⣾⣿⣿⠿⠟⠛⠋⠛⢿⣿⣿⠻⣿⣿⣿⣿⡿⠀
#  ⠀⠀⠀⠀⠀⠀⠀⢀⠇⠀⢠⣿⣟⣭⣤⣶⣦⣄⡀⠀⠀⠈⠻⠀⠘⣿⣿⣿⠇⠀
#  ⠀⠀⠀⠀⠀⠱⠤⠊⠀⢀⣿⡿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠘⣿⠏⠀⠀                             𓆩♕𓆪
#  ⠀⠀⠀⠀⠀⡄⠀⠀⠀⠘⢧⡀⠀⠀⠸⣿⣿⣿⠟⠀⠀⠀⠀⠀⠀⠐⠋⠀⠀⠀                     𓄂 oussama ezzaou𓆃
#  ⠀⠀⠀⠀⠀⠘⠄⣀⡀⠸⠓⠀⠀⠀⠠⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

# ====[ Modules: >=============================================================
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from dataclasses import dataclass
import json


# ==== [ Screen : data class >=================================================
@dataclass
class Screen:
    height:             int = 600
    width:              int = 1200

    def get_center(self):
        return self.width / 2, self.height / 2


# ==== [ Paddle : data class >=================================================
@dataclass
class Paddle:
    x:                  int
    y:                  int
    width:              int = 20
    height:             int = 100


# ==== [ Paddle : data class >=================================================
@dataclass
class Player:
    id:                 str
    paddle:             Paddle
    score:              int


# ==== [ Ball : data class >===================================================
@dataclass
class Ball:
    x:                  int
    y:                  int
    step_x:             float
    step_y:             float
    radius:             int


# ==== [ Game : data class >===================================================
@dataclass
class Game:

    screen:             Screen
    right_player:       Player
    left_player:        Player
    ball:               Ball
    room_id:            str
    state:              str = "START"

    # ==== [ init: game_init >=================================================
    def init(self):
        self.broadcast_to_players({
            "type": "gameplay_init",
            "ball": [self.ball.x, self.ball.y],
            "score": [self.left_player.score, self.right_player.score],
            "paddle_x": [self.left_player.paddle.x, self.right_player.paddle.x]
        })
        return (self)

    # ==== [ update_state: game state based on paddle & ball states >==========
    def update_state(self, event):
        self.update_paddle_state(event)
        self.update_ball_state()
        return (self)

    # ==== [update_paddle_state: update paddle state based on event >==========
    def update_paddle_state(self, paddle_event):
        if paddle_event is None:
            return
        players = [self.left_player, self.right_player]
        paddle_y = json.loads(paddle_event)
        for player in players:
            if player.id in paddle_y:
                player.paddle.y = paddle_y[player.id]
                self.broadcast_to_players({
                    "type": "paddle_state",
                    "player_id": player.id,
                    "paddle_y": player.paddle.y,
                })

    # ==== [ update_ball_state: >==============================================
    def update_ball_state(self):
        self.ball.x += self.ball.step_x
        self.ball.y += self.ball.step_y
        self.top_bottom_collision()
        self.left_right_collision()
        self.broadcast_to_players({
            "type": "ball_state",
            "ball": [self.ball.x, self.ball.y],
        })
        print(f"{self.ball.x, self.ball.y}")

    # ==== [ top_bottom_collision: >===========================================
    def top_bottom_collision(self):
        min, max = self.ball.radius, self.screen.height - self.ball.radius
        if self.ball.y not in range(min, max + 1):
            self.ball.y = min if self.ball.y <= min else max
            self.ball.step_y *= -1

    # ==== [ left_right_collision: >===========================================
    def left_right_collision(self):
        min, max = self.ball.radius, self.screen.width - self.ball.radius
        if self.ball.x not in range(min, max + 1):
            self.ball.x = min if self.ball.x <= min else max
            self.ball.step_x *= -1

    # ==== [ reinitialize: reinitialize game for another round >===============
    def reinitialize(self):
        pass

    # ==== [ broadcast_to_players: >===========================================
    def broadcast_to_players(self, data):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(self.room_id, data)

    # ==== [ get_history: return history of game >=============================
    def get_history(self):
        pass
