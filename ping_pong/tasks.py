#  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣦⣴⣶⣾⣿⣶⣶⣶⣶⣦⣤⣄⠀⠀⠀⠀⠀⠀⠀
#  ⠀⠀⠀⠀⠀⠀⠀⢠⡶⠻⠛⠟⠋⠉⠀⠈⠤⠴⠶⠶⢾⣿⣿⣿⣷⣦⠄⠀⠀⠀                𓐓  tasks.py 𓐔           
#  ⠀⠀⠀⠀⠀⢀⠔⠋⠀⠀⠤⠒⠒⢲⠀⠀⠀⢀⣠⣤⣤⣬⣽⣿⣿⣿⣷⣄⠀⠀
#  ⠀⠀⠀⣀⣎⢤⣶⣾⠅⠀⠀⢀⡤⠏⠀⠀⠀⠠⣄⣈⡙⠻⢿⣿⣿⣿⣿⣿⣦⠀   Student: oezzaou <oezzaou@student.1337.ma>
#  ⢀⠔⠉⠀⠊⠿⠿⣿⠂⠠⠢⣤⠤⣤⣼⣿⣶⣶⣤⣝⣻⣷⣦⣍⡻⣿⣿⣿⣿⡀
#  ⢾⣾⣆⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠉⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
#  ⠀⠈⢋⢹⠋⠉⠙⢦⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇       Created: 2024/11/24 13:06:31 by oezzaou
#  ⠀⠀⠀⠑⠀⠀⠀⠈⡇⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇       Updated: 2024/12/14 03:26:13 by oezzaou
#  ⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⢀⣾⣿⣿⠿⠟⠛⠋⠛⢿⣿⣿⠻⣿⣿⣿⣿⡿⠀ ⠀⠀⠀⠀⠀⠀⠀⢀⠇⠀⢠⣿⣟⣭⣤⣶⣦⣄⡀⠀⠀⠈⠻⠀⠘⣿⣿⣿⠇⠀
#  ⠀⠀⠀⠀⠀⠱⠤⠊⠀⢀⣿⡿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠘⣿⠏⠀⠀                             𓆩♕𓆪
#  ⠀⠀⠀⠀⠀⡄⠀⠀⠀⠘⢧⡀⠀⠀⠸⣿⣿⣿⠟⠀⠀⠀⠀⠀⠀⠐⠋⠀⠀⠀                     𓄂 oussama ezzaou𓆃
#  ⠀⠀⠀⠀⠀⠘⠄⣀⡀⠸⠓⠀⠀⠀⠠⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

# ====<[ Modules: ]>===========================================================
from .game import Game, Player, Paddle, Ball, Screen
from celery import shared_task
import requests
import redis
import time
import json


# ====<[ start_gameplay: game task handled by celery ]>========================
@shared_task
def start_gameplay(left_player_id, right_player_id, room_id, game_cache):
    game = game_init(left_player_id, right_player_id, room_id)
    results = game_event_loop(game, game_cache)
    game_register_results(results)


# ====<[ game_init: initiate game ]>===========================================
def game_init(left_player_id, right_player_id, room_id):
    screen = Screen(600, 1200)
    cx, cy = screen.get_center()
    left_paddle = Paddle(x=0, y=cy, side=1)
    right_paddle = Paddle(x=screen.width, y=cy, side=-1)
    left_player = Player(id=left_player_id, paddle=left_paddle, score=0)
    right_player = Player(id=right_player_id, paddle=right_paddle, score=0)
    ball = Ball(x=cx, y=cy, radius=10, speed=9, speed_x=3, speed_y=3)
    game = Game(screen, left_player, right_player, ball, room_id)
    return game.init()


# ====<[ game_event_loop: ]>===================================================
def game_event_loop(game, game_cache):
    redis_conn = redis.StrictRedis("redis", 6379, decode_responses=True)
    fps = 1 / 60

    while game.state != "END":
        start_time = time.time()
        event = redis_conn.hgetall(game_cache)
        game = game.update_state(event)
        if game.state == "STOP":
            game.stop()
        if game.state == "RESTART":
            game.reinit()
            redis_conn.delete(game_cache)
        elapsed_time = time.time() - start_time
        time.sleep(max(0, fps - elapsed_time))
    redis_conn.close()
    return game.end()


# ====<[ game_register_history ]>==============================================
def game_register_results(results):
    data = json.dumps(results)
    headers = {"Authorization": "Bearer your-token"}
    url = "http://profileM_service:8080/"
    try:
        response = requests.post(url=url, json=data, headers=headers)
    except requests.RequestException as msg:
        print(f"{str(msg)}")
