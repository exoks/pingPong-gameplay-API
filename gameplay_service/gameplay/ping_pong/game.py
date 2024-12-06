#  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣦⣴⣶⣾⣿⣶⣶⣶⣶⣦⣤⣄⠀⠀⠀⠀⠀⠀⠀
#  ⠀⠀⠀⠀⠀⠀⠀⢠⡶⠻⠛⠟⠋⠉⠀⠈⠤⠴⠶⠶⢾⣿⣿⣿⣷⣦⠄⠀⠀⠀                 𓐓  game.py 𓐔           
#  ⠀⠀⠀⠀⠀⢀⠔⠋⠀⠀⠤⠒⠒⢲⠀⠀⠀⢀⣠⣤⣤⣬⣽⣿⣿⣿⣷⣄⠀⠀
#  ⠀⠀⠀⣀⣎⢤⣶⣾⠅⠀⠀⢀⡤⠏⠀⠀⠀⠠⣄⣈⡙⠻⢿⣿⣿⣿⣿⣿⣦⠀   Student: oezzaou <oezzaou@student.1337.ma>
#  ⢀⠔⠉⠀⠊⠿⠿⣿⠂⠠⠢⣤⠤⣤⣼⣿⣶⣶⣤⣝⣻⣷⣦⣍⡻⣿⣿⣿⣿⡀
#  ⢾⣾⣆⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠉⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
#  ⠀⠈⢋⢹⠋⠉⠙⢦⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇       Created: 2024/11/24 07:24:58 by oezzaou
#  ⠀⠀⠀⠑⠀⠀⠀⠈⡇⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇       Updated: 2024/12/06 08:53:37 by oezzaou
#  ⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⢀⣾⣿⣿⠿⠟⠛⠋⠛⢿⣿⣿⠻⣿⣿⣿⣿⡿⠀
#  ⠀⠀⠀⠀⠀⠀⠀⢀⠇⠀⢠⣿⣟⣭⣤⣶⣦⣄⡀⠀⠀⠈⠻⠀⠘⣿⣿⣿⠇⠀
#  ⠀⠀⠀⠀⠀⠱⠤⠊⠀⢀⣿⡿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠘⣿⠏⠀⠀                             𓆩♕𓆪
#  ⠀⠀⠀⠀⠀⡄⠀⠀⠀⠘⢧⡀⠀⠀⠸⣿⣿⣿⠟⠀⠀⠀⠀⠀⠀⠐⠋⠀⠀⠀                     𓄂 oussama ezzaou𓆃
#  ⠀⠀⠀⠀⠀⠘⠄⣀⡀⠸⠓⠀⠀⠀⠠⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

# ====[ Modules: >=============================================================
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from dataclasses import dataclass, field
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
    _default:           dict = field(init=False, repr=False)

    def __post_init__(self):
        self.y -= (self.height / 2)
        self._default = {
            "x": self.x,
            "y": self.y,
        }

    def rest(self):
        self.x, self.y = self._default['x'], self._default['y']

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
    _default:           dict = field(init=False, repr=False)

    def __post_init__(self):
        self._default = {
            "x": self.x,
            "y": self.y,
            "speed": self.speed,
            "speed_x": self.speed_x,
            "speed_y": self.speed_y,
        }

    def reset(self):
        self.x, self.y = self._default['x'], self._default['y']
        self.speed = self._default['speed']
        self.speed_x = self._default['speed_x']
        self.speed_y = self._default['speed_y']

    def top(self):
        return self.y - self.radius

    def bottom(self):
        return self.y + self.radius

    def left(self):
        return self.x - self.radius

    def right(self):
        return self.x + self.radius


# ==== [ Game : data class >===================================================
class Game:

    screen:             Screen
    left_player:        Player
    right_player:       Player
    ball:               Ball
    room_id:            str
    state:              str = "START"

    # ==== [ __init__(): constructor >=========================================
    def __init__(self, screen, left_player, right_player, ball, room_id):
        self.screen = screen
        self.left_player = left_player
        self.right_player = right_player
        self.ball = ball
        self.room_id = room_id

    # ==== [ init: game_init >=================================================
    def init(self):
        async_to_sync(self.broadcast_to_players)({
            "type": "gameplay_init",
            "ball": [self.ball.x, self.ball.y],
            "score": [self.left_player.score, self.right_player.score],
            "paddle_x": [self.left_player.paddle.x, self.right_player.paddle.x]
        })
        return (self)

    # ==== [ update_state: game state based on paddle & ball states >==========
    def update_state(self, paddle_event):
        self.update_paddle_state(paddle_event)
        self.update_ball_state()
        return (self)

    # ==== [update_paddle_state: update paddle state based on event >==========
    def update_paddle_state(self, paddle_event):
        players = [self.left_player, self.right_player]
        for player in players:
            if player.id in paddle_event:
                player.paddle.y = int(paddle_event[player.id])

    # ==== [ update_ball_state: >==============================================
    def update_ball_state(self):
        self.ball.x += int(self.ball.speed_x)
        self.ball.y += int(self.ball.speed_y)
        self.top_bottom_collision()
        self.paddles_collision()
        self.left_right_collision()
        async_to_sync(self.broadcast_to_players)({
            "type": "ball_state",
            "ball": [self.ball.x, self.ball.y],
        })

    # ==== [ top_bottom_collision: >===========================================
    def top_bottom_collision(self):
        min, max = self.ball.radius, self.screen.height - self.ball.radius
        if self.ball.y not in range(min, max + 1):
            self.ball.speed_y *= -1

    # ==== [ left_right_collision: >===========================================
    def left_right_collision(self):
        min, max = -self.ball.radius, self.screen.width + self.ball.radius
        if self.ball.x not in range(min, max + 1):
            self.left_player.score += int(self.ball.x > max)
            self.right_player.score += int(self.ball.x < min)
            isEnd = self.left_player.score == 6 or self.right_player.score == 6
            self.state = "END" if isEnd is True else "RESTART"

    # ==== [ paddles_collision: check collistion with paddles >================
    def paddles_collision(self):
        paddles = [self.left_player.paddle, self.right_player.paddle]
        paddle = paddles[self.ball.x > self.screen.width / 2]
        collision = (self.ball.bottom() > paddle.top() and
                     self.ball.top() < paddle.bottom() and
                     self.ball.right() > paddle.left() and
                     self.ball.left() < paddle.right())
        if collision is True:
            collide_point = (2 * (self.ball.y - paddle.y) / paddle.height) - 1
            α = (math.pi / 8) * collide_point
            self.ball.speed_x = paddle.side * self.ball.speed * math.cos(α)
            self.ball.speed_y = self.ball.speed * math.sin(α)
            self.ball.speed += 0.1

    # ==== [ reinit: reinitialize game for another round >=====================
    def reinit(self):
        self.state = "START"
        self.ball.reset()
        self.left_player.paddle.rest()
        self.right_player.paddle.rest()
        async_to_sync(self.broadcast_to_players)({
            "type": "gameplay_reinit",
            "ball": [self.ball.x, self.ball.y],
            "score": [self.left_player.score, self.right_player.score],
            "paddle_x": [self.left_player.paddle.x, self.right_player.paddle.x]
        })
        # print("[SERVER: REINIT]> reinit the game")
        return self

    # ==== [ end: broadcast game_end & return game results >===================
    def end(self):
        results = {
            self.left_player.id: self.left_player.score,
            self.right_player.id: self.right_player.score,
        }
        async_to_sync(self.broadcast_to_players)({
            "type": "gameplay_end",
            "score": [self.left_player.score, self.right_player.score],
        })
        return results

    # ==== [ broadcast_to_players: >===========================================
    async def broadcast_to_players(self, data):
        channel_layer = get_channel_layer()
        await channel_layer.group_send(self.room_id, data)
