from django.urls import path

from .consumers import *

ws_urlpatterns = [
    path("ws/chatws/", WSConsumerChat.as_asgi()),
    path("ws/chatws/<str:room>/", WSConsumerChatChannels.as_asgi())
]