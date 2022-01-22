from django.contrib import admin

# Register your models here.
from .models import StudentData, FriendRequest, Notification

admin.site.register(StudentData)
admin.site.register(FriendRequest)
admin.site.register(Notification)
