import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from django.db import models

STANDARD = (
    ('I', 'I'),
    ('II', 'II'),
    ('III', 'III'),
    ('IV', 'IV'),
    ('V', 'V'),
    ('VI', 'VI'),
    ('VII', 'VII'),
    ('VIII', 'VIII'),
    ('IX', 'IX'),
    ('X', 'X'),
    ('XI', 'XI'),
    ('XII', 'XII'),
)

NOTIFICATIONS = (
    ('Friend Request', 'Friend Request'),
)


class StudentData(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    prn = models.CharField(max_length=16, unique=True)
    full_name = models.CharField(max_length=80)
    mother_name = models.CharField(max_length=20)
    roll_number = models.IntegerField(null=True, blank=True)
    standard = models.CharField(max_length=20, choices=STANDARD, null=True, blank=True)
    profile = models.ImageField(upload_to='profile/', default='avatar.png')
    tag = models.CharField(max_length=50, null=True, blank=True)
    account_scope = models.BooleanField(default=True)
    friends = models.ManyToManyField(User, blank=True, related_name='friends')

    def __str__(self):
        return f"{self.id}"


class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    status = models.BooleanField(default=True, null=False, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"


class Notification(models.Model):
    notify_sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notify_sender')
    notify_receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notify_receiver')
    message = models.CharField(max_length=100, choices=NOTIFICATIONS, default='')
    is_seen = models.BooleanField(default=False, blank=False, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"

