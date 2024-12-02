#  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣦⣴⣶⣾⣿⣶⣶⣶⣶⣦⣤⣄⠀⠀⠀⠀⠀⠀⠀
#  ⠀⠀⠀⠀⠀⠀⠀⢠⡶⠻⠛⠟⠋⠉⠀⠈⠤⠴⠶⠶⢾⣿⣿⣿⣷⣦⠄⠀⠀⠀                 𓐓  game.py 𓐔           
#  ⠀⠀⠀⠀⠀⢀⠔⠋⠀⠀⠤⠒⠒⢲⠀⠀⠀⢀⣠⣤⣤⣬⣽⣿⣿⣿⣷⣄⠀⠀
#  ⠀⠀⠀⣀⣎⢤⣶⣾⠅⠀⠀⢀⡤⠏⠀⠀⠀⠠⣄⣈⡙⠻⢿⣿⣿⣿⣿⣿⣦⠀   Student: oezzaou <oezzaou@student.1337.ma>
#  ⢀⠔⠉⠀⠊⠿⠿⣿⠂⠠⠢⣤⠤⣤⣼⣿⣶⣶⣤⣝⣻⣷⣦⣍⡻⣿⣿⣿⣿⡀
#  ⢾⣾⣆⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠉⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
#  ⠀⠈⢋⢹⠋⠉⠙⢦⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇       Created: 2024/11/24 07:24:58 by oezzaou
#  ⠀⠀⠀⠑⠀⠀⠀⠈⡇⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇       Updated: 2024/12/01 21:13:37 by oezzaou
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
import math


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
    side:               int
    width:              int = 20
    height:             int = 100

    def top(self):
        return self.y

    def bottom(self):
        return self.y + self.height

    def left(self):
        return self.x if self.side == 1 else self.x - self.width

    def right(self):
        return self.x if self.side == -1 else self.x + self.width


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
    radius:             int
    speed:              float
    speed_x:            float
    speed_y:            float

    def top(self):
        return self.y - self.radius

    def bottom(self):
        return self.y + self.radius

    def left(self):
        return self.x - self.radius

    def right(self):
        return self.x + self.radius


# ==== [ Game : data class >===================================================
@dataclass
class Game:

    screen:             Screen
    left_player:        Player
    right_player:       Player
    ball:               Ball
    room_id:            str
    state:              str = "START"

    # ==== [ init: game_init >=================================================
    def init(self):
        cx, cy = self.screen.get_center()
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

    # ==== [ update_ball_state: >==============================================
    def update_ball_state(self):
        self.ball.x += self.ball.speed_x
        self.ball.y += self.ball.speed_y
        print(f"{self.ball.x}:{self.ball.y}")
        self.top_bottom_collision()
        self.paddles_collision()
        self.left_right_collision()
        self.broadcast_to_players({
            "type": "ball_state",
            "ball": [self.ball.x, self.ball.y],
        })

    # ==== [ top_bottom_collision: >===========================================
    def top_bottom_collision(self):
        min, max = self.ball.radius, self.screen.height - self.ball.radius
        if self.ball.y not in range(min, max + 1):
            print("[BALL: COLLISION]> collision with TOP/BOTTOM")
            self.ball.speed_y *= -1

    # ==== [ left_right_collision: >===========================================
    def left_right_collision(self):
        min, max = self.ball.radius, self.screen.width - self.ball.radius
        if self.ball.x not in range(min, max + 1):
            self.ball.x = min if self.ball.x <= min else max
            self.left_player.score += int(self.ball.x == min)
            self.right_player.score += int(self.ball.x == max)
            self.state = "RESTART"
            # line for test (removed later)
            self.ball.speed_x *= -1

    # ==== [ paddles_collision: check collistion with paddles >================
    def paddles_collision(self):
        paddles = [self.left_player.paddle, self.right_player.paddle]
        paddle = paddles[self.ball.x > self.screen.width / 2]
        collision = (self.ball.bottom() > paddle.top() and
                     self.ball.top() < paddle.bottom() and
                     self.ball.right() > paddle.left() and
                     self.ball.left() < paddle.right())
        if collision is True:
            print(f"[GAME: PADDLE] > Collision: {paddle.side}")
            collide_point = self.ball.y - (paddle.y + paddle.height / 2)
            collide_point /= paddle.height / 2
            # collide_point = ((2 * self.ball.y - paddle.y) / paddle.height) - 1
            α = (math.pi / 4) * collide_point
            self.ball.speed_x = int(paddle.side * self.ball.speed * math.cos(α))
            self.ball.speed_y = int(self.ball.speed * math.sin(α))
            self.ball.speed += 0.1
            # print(f"[SPEED: x] > {self.ball.speed_x}")
            # print(f"[GAME: ]> {self.ball.speed_x}:{self.ball.speed_y}")

    # ==== [ reinit: reinitialize game for another round >=====================
    def reinit(self, new_game_state):
        self.state = new_game_state
        self.broadcast_to_players({
            "type": "gameplay_reinit",
            "ball": [self.screen.width / 2, self.screen.height / 2],
            "score": [self.left_player.score, self.right_player.score],
            "paddle_x": [self.left_player.paddle.x, self.right_player.paddle.x]
        })
        print("[SERVER: REINIT]> reinit the game")
        return (self)

    # ==== [ broadcast_to_players: >===========================================
    def broadcast_to_players(self, data):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(self.room_id, data)

    # ==== [ get_history: return history of game >=============================
    def get_history(self):
        pass

# collide_point = self.ball.y - (paddle.y + paddle.height / 2)
# collide_point = collide_point / (paddle.height / 2)
