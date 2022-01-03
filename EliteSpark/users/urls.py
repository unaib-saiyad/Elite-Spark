from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserAuth.as_view(), name='user'),
]

