from django.urls import path, re_path

from . import consumers

websocket_urlpatterns = [
    path(r'notification/<str:user_id>', consumers.NotificationConsumer.as_asgi()),
]
