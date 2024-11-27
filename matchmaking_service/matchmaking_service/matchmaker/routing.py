from django.urls import re_path
from . import player_consumer


# we can pass a pattern using regex to define a set of sockets
# the socket url is url = "ws://localhost:8000/ws/entrance/"
# websocket_urlpatterns = [
#     re_path('ws/entrance/', consumers.PlayerHandler.as_asgi()),
# ]

websocket_urlpatterns = [
    re_path(r'ws/entrance/$', player_consumer.PlayerConsumer.as_asgi()),
]
