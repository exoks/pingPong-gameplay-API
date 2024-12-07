#  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣦⣴⣶⣾⣿⣶⣶⣶⣶⣦⣤⣄⠀⠀⠀⠀⠀⠀⠀
#  ⠀⠀⠀⠀⠀⠀⠀⢠⡶⠻⠛⠟⠋⠉⠀⠈⠤⠴⠶⠶⢾⣿⣿⣿⣷⣦⠄⠀⠀⠀                𓐓  tasks.py 𓐔           
#  ⠀⠀⠀⠀⠀⢀⠔⠋⠀⠀⠤⠒⠒⢲⠀⠀⠀⢀⣠⣤⣤⣬⣽⣿⣿⣿⣷⣄⠀⠀
#  ⠀⠀⠀⣀⣎⢤⣶⣾⠅⠀⠀⢀⡤⠏⠀⠀⠀⠠⣄⣈⡙⠻⢿⣿⣿⣿⣿⣿⣦⠀   Student: oezzaou <oezzaou@student.1337.ma>
#  ⢀⠔⠉⠀⠊⠿⠿⣿⠂⠠⠢⣤⠤⣤⣼⣿⣶⣶⣤⣝⣻⣷⣦⣍⡻⣿⣿⣿⣿⡀
#  ⢾⣾⣆⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠉⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
#  ⠀⠈⢋⢹⠋⠉⠙⢦⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇       Created: 2024/12/06 08:10:30 by oezzaou
#  ⠀⠀⠀⠑⠀⠀⠀⠈⡇⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇       Updated: 2024/12/07 17:09:56 by oezzaou
#  ⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⢀⣾⣿⣿⠿⠟⠛⠋⠛⢿⣿⣿⠻⣿⣿⣿⣿⡿⠀
#  ⠀⠀⠀⠀⠀⠀⠀⢀⠇⠀⢠⣿⣟⣭⣤⣶⣦⣄⡀⠀⠀⠈⠻⠀⠘⣿⣿⣿⠇⠀
#  ⠀⠀⠀⠀⠀⠱⠤⠊⠀⢀⣿⡿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠘⣿⠏⠀⠀                             𓆩♕𓆪
#  ⠀⠀⠀⠀⠀⡄⠀⠀⠀⠘⢧⡀⠀⠀⠸⣿⣿⣿⠟⠀⠀⠀⠀⠀⠀⠐⠋⠀⠀⠀                     𓄂 oussama ezzaou𓆃
#  ⠀⠀⠀⠀⠀⠘⠄⣀⡀⠸⠓⠀⠀⠀⠠⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

# ==== [ Modules: ] ===========================================================
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from celery import shared_task
import redis
import time

# ==== [ Gloabl: ] ============================================================
redis_conn = redis.StrictRedis(host='redis', port=6379, decode_responses=True)


# ====[ matchmaker: task to find player match >================================
@shared_task
def matchmaker(room_id, player_cache, player_id, player_rank):
    # NOTE: > [TEST BlOCK]
    all_players = redis_conn.zrange(player_cache, 0, -1, withscores=True)
    print(f"[TASK] All players: {all_players}")
    # NOTE: > [TEST BLOCK]
    opponent = search_for_opponent(player_cache, player_rank, rank_range=10)
    print(f"[MATCH_MAKING: ] > opponent {opponent}")  # NOTE: > [for test]
    if opponent is not None:
        broadcast_matching(room_id, player_id, opponent)
    else:
        wait_for_opponent(room_id, player_cache, player_id, player_rank)
    redis_conn.close()


# ====[ search_for_opponent: search in player_cache >==========================
def search_for_opponent(player_cache, player_rank, rank_range):
    min_rank = int(player_rank) - rank_range
    max_rank = int(player_rank) + rank_range
    lua_script = """
        local matches

        matches = redis.call(
        'ZRANGEBYSCORE', KEYS[1], ARGV[1], ARGV[2], "WITHSCORES")
        if #matches > 0 then
            redis.call('ZREM', KEYS[1], matches[1])
            return matches[1]
        end
        return nil
        """
    return redis_conn.eval(lua_script, 1, player_cache, min_rank, max_rank)


# ====[ wait_for_opponet: wait for match in 30 s >============================
def wait_for_opponent(room_id, player_cache, player_id, player_rank):
    redis_conn.zadd(player_cache, {player_id: player_rank})
    print(f"[TASK] Added {player_id} to players")  # NOTE: > [for test]
    for timer in range(0, 30):
        if redis_conn.zscore(player_cache, player_id) is None:
            break
        time.sleep(1)
    if redis_conn.zrem(player_cache, player_id) == 1:
        broadcast_matching(room_id, player_id, None)


# ====[ broadcast_matching: broadcast matching to room_id >====================
def broadcast_matching(room_id, player_id, opponent_id):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(room_id, {
        "type": "match_found",
        "match": f"{player_id}{opponent_id}",
        "room_id": f"{player_id}{opponent_id}-{int(time.time())}",
    })
