from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from celery import shared_task
import redis
import time

# b'str', refer to binary string representation, that's why we use decode
r = redis.StrictRedis(host='redis', port=6379, decode_responses=True)
channel_layer = get_channel_layer()
players_set = "players"
matchmaker_group = "matchmaker"


@shared_task
def matchmaker(player_id, player_rank):
    global r, players_set

    # print(f"[TASK] Starting search for player_id={player_id}, player_rank={player_rank}")
    all_players = r.zrange(players_set, 0, -1, withscores=True)
    print(f"[TASK] All players: {all_players}")
    opponent = search_for_opponent(player_rank, 10)
    print(f"[MATCH_MAKING: ] > opponent {opponent}")
    if opponent is not None:
        broadcast_matching(player_id, opponent)
    else:
        wait_for_opponent(player_id, player_rank)


def search_for_opponent(player_rank, rank_range):
    global players_set

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
    return r.eval(lua_script, 1, players_set, min_rank, max_rank)


# no match: player add it self & wait for 30s to get matched otherwise remove
# it self a play against ia opponent
def wait_for_opponent(player_id, player_rank):
    global players_set

    r.zadd(players_set, {player_id: player_rank})
    print(f"[TASK] Added {player_id} to players")
    for timer in range(0, 30):
        if r.zscore(players_set, player_id) is None:
            break
        time.sleep(1)
    if r.zrem(players_set, player_id) == 1:
        broadcast_matching(player_id, None)


# broadcast to matchmaker_group the matches
def broadcast_matching(player_id, opponent_id):
    global channel_layer, matchmaker_group

    async_to_sync(channel_layer.group_send)(
        matchmaker_group,
        {
            "type": "match_found",
            "match": f"{player_id}{opponent_id}",
            "room_id": f"{player_id}{opponent_id}-{int(time.time())}",
        },
    )
