#  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣦⣴⣶⣾⣿⣶⣶⣶⣶⣦⣤⣄⠀⠀⠀⠀⠀⠀⠀
#  ⠀⠀⠀⠀⠀⠀⠀⢠⡶⠻⠛⠟⠋⠉⠀⠈⠤⠴⠶⠶⢾⣿⣿⣿⣷⣦⠄⠀⠀⠀                 𓐓  game.py 𓐔           
#  ⠀⠀⠀⠀⠀⢀⠔⠋⠀⠀⠤⠒⠒⢲⠀⠀⠀⢀⣠⣤⣤⣬⣽⣿⣿⣿⣷⣄⠀⠀
#  ⠀⠀⠀⣀⣎⢤⣶⣾⠅⠀⠀⢀⡤⠏⠀⠀⠀⠠⣄⣈⡙⠻⢿⣿⣿⣿⣿⣿⣦⠀   Student: oezzaou <oezzaou@student.1337.ma>
#  ⢀⠔⠉⠀⠊⠿⠿⣿⠂⠠⠢⣤⠤⣤⣼⣿⣶⣶⣤⣝⣻⣷⣦⣍⡻⣿⣿⣿⣿⡀
#  ⢾⣾⣆⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠉⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
#  ⠀⠈⢋⢹⠋⠉⠙⢦⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇       Created: 2024/11/24 07:24:58 by oezzaou
#  ⠀⠀⠀⠑⠀⠀⠀⠈⡇⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇       Updated: 2024/12/14 03:27:03 by oezzaou
#  ⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⢀⣾⣿⣿⠿⠟⠛⠋⠛⢿⣿⣿⠻⣿⣿⣿⣿⡿⠀
#  ⠀⠀⠀⠀⠀⠀⠀⢀⠇⠀⢠⣿⣟⣭⣤⣶⣦⣄⡀⠀⠀⠈⠻⠀⠘⣿⣿⣿⠇⠀
#  ⠀⠀⠀⠀⠀⠱⠤⠊⠀⢀⣿⡿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠘⣿⠏⠀⠀                             𓆩♕𓆪
#  ⠀⠀⠀⠀⠀⡄⠀⠀⠀⠘⢧⡀⠀⠀⠸⣿⣿⣿⠟⠀⠀⠀⠀⠀⠀⠐⠋⠀⠀⠀                     𓄂 oussama ezzaou𓆃
#  ⠀⠀⠀⠀⠀⠘⠄⣀⡀⠸⠓⠀⠀⠀⠠⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

# ====<[ Modules: ]>===========================================================
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from dataclasses import dataclass, field
import math
import time


# ====<[ Screen : data class ]>================================================
@dataclass
class Screen:
    height:             int = 600
    width:              int = 1200

    def get_center(self):
        return self.width / 2, self.height / 2


# ====<[ Paddle : data class ]>================================================
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

    def reset(self):
        self.x, self.y = self._default['x'], self._default['y']

    def top(self):
        return self.y

    def bottom(self):
        return self.y + self.height

    def left(self):
        return self.x if self.side == 1 else self.x - self.width

    def right(self):
        return self.x if self.side == -1 else self.x + self.width


# ====<[ Paddle : data class ]>================================================
@dataclass
class Player:
    id:                 str
    paddle:             Paddle
    score:              int
    state:              str = "unkown"
    timer:              int = 30
    _default:           dict = field(init=False, repr=False)

    def __post_init__(self):
        self._default = {
            "timer": self.timer,
        }

    def reset(self):
        self.paddle.reset()
        self.timer = self._default["timer"]


# ====<[ Ball : data class ]>==================================================
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


# ====<[ Game : data class ]>==================================================
class Game:

    screen:             Screen
    left_player:        Player
    right_player:       Player
    ball:               Ball
    room_id:            str
    state:              str = "START"
    max_score:          int = 6

    # ====<[ __init__(): constructor ]>========================================
    def __init__(self, screen, left_player, right_player, ball, room_id):
        self.screen = screen
        self.left_player = left_player
        self.right_player = right_player
        self.ball = ball
        self.room_id = room_id

    # ====<[ init: game_init ]>================================================
    def init(self):
        async_to_sync(self.broadcast_to_players)({
            "type": "gameplay_init",
            "ball": [self.ball.x, self.ball.y],
            "score": [self.left_player.score, self.right_player.score],
            "paddle_x": [self.left_player.paddle.x, self.right_player.paddle.x]
        })
        return (self)

    # ====<[ update_state: game state based on paddle & ball states ]>=========
    def update_state(self, event):
        self.update_player_state(event)
        # print(f"[GAME: STATE]: {self.state}")
        if self.state != "STOP":
            self.update_paddle_state(event)
            self.update_ball_state()
        return (self)

    # ====<[ update_player_state: ]>===========================================
    def update_player_state(self, event_dict):
        players, states = [self.left_player, self.right_player], []
        for player in players:
            player_state = f"{player.id}_state"
            if player_state in event_dict:
                player.state = event_dict.pop(player_state)
            states.append(player.state)
        self.state = "START" if "unavailable" not in states else "STOP"

    # ====<[update_paddle_state: update paddle state based on event ]>=========
    def update_paddle_state(self, event_dict):
        players = [self.left_player, self.right_player]
        for player in players:
            paddle_y = f"{player.id}_paddle_y"
            if paddle_y in event_dict:
                player.paddle.y = int(event_dict.pop(paddle_y))

    # ====<[ update_ball_state: ]>=============================================
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

    # ====<[ top_bottom_collision: ]>==========================================
    def top_bottom_collision(self):
        min, max = self.ball.radius, self.screen.height - self.ball.radius
        if self.ball.y not in range(min, max + 1):
            self.ball.speed_y *= -1

    # ====<[ left_right_collision: ]>==========================================
    def left_right_collision(self):
        scores = [self.left_player.score, self.right_player.score]
        self.state = "END" if self.max_score in scores else self.state
        min, max = -self.ball.radius, self.screen.width + self.ball.radius
        if self.ball.x not in range(min, max + 1):
            self.left_player.score += int(self.ball.x > max)
            self.right_player.score += int(self.ball.x < min)
            self.state = "RESTART"

    # ====<[ paddles_collision: check collistion with paddles ]>===============
    def paddles_collision(self):
        paddles = [self.left_player.paddle, self.right_player.paddle]
        paddle = paddles[self.ball.x > self.screen.width / 2]
        collision = (self.ball.bottom() > paddle.top() and
                     self.ball.top() < paddle.bottom() and
                     self.ball.right() > paddle.left() and
                     self.ball.left() < paddle.right())
        if collision is True:
            collide_point = (2 * (self.ball.y - paddle.y) / paddle.height) - 1
            α = (math.pi / 5) * collide_point
            self.ball.speed_x = paddle.side * self.ball.speed * math.cos(α)
            self.ball.speed_y = self.ball.speed * math.sin(α)
            self.ball.speed += 0.2

    # ====<[ reinit: reinitialize game for another round ]>====================
    def reinit(self):
        self.ball.reset()
        self.left_player.reset()
        self.right_player.reset()
        async_to_sync(self.broadcast_to_players)({
            "type": "gameplay_reinit",
            "ball": [self.ball.x, self.ball.y],
            "score": [self.left_player.score, self.right_player.score],
            "paddle_x": [self.left_player.paddle.x, self.right_player.paddle.x]
        })
        # print("[SERVER: REINIT]> reinit the game")

    # ====<[stop: stop the game one second ]>==================================
    def stop(self):
        players = [self.left_player, self.right_player]
        time_sleep = 1
        for index, player in enumerate(players):
            if player.state == "unavailable":
                time.sleep(time_sleep)
                player.timer -= time_sleep
                if player.timer == 0:
                    players[0 if index > 0 else 1].score = self.max_score
                    self.state = "END"
                async_to_sync(self.broadcast_to_players)({
                    "type": "gameplay_stop",
                    "player_id": player.id,
                    "timer": player.timer,
                })
                # print(f"sleep: {player.timer}")

    # ====<[ end: broadcast game_end & return game results ]>==================
    def end(self):
        players = [self.left_player, self.right_player]
        winner, loser = (1, 0) if players[0].score < self.max_score else (0, 1)
        results = {
            "winner_id": players[winner].id,
            "loser_id": players[loser].id,
            "winner_score": players[winner].score,
            "loser_score": players[loser].score,
        }
        async_to_sync(self.broadcast_to_players)({
            "type": "gameplay_end",
            "winner_id": results['winner_id'],
            "loser_id": results['loser_id'],
            "winner_score": results['winner_score'],
            "loser_score": results['loser_score'],
        })
        return results

    # ====<[ broadcast_to_players: ]>==========================================
    async def broadcast_to_players(self, data):
        channel_layer = get_channel_layer()
        await channel_layer.group_send(self.room_id, data)
