from rest_framework import serializers
from .models import StudentData, FriendRequest


class StudentDataSerilizer(serializers.ModelSerializer):
    user = serializers.CharField(source='student.username', read_only=True)
    friends_count = serializers.SerializerMethodField('get_friends_count')

    class Meta:
        model = StudentData
        fields = '__all__'

    def get_friends_count(self, obj):
        return obj.friends.all().count()


class FriendRequestSerilizer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.username', read_only=True)
    receiver = serializers.CharField(source='receiver.username', read_only=True)
    sender_profile = serializers.SerializerMethodField('get_sender_profile')
    timestamp = serializers.SerializerMethodField('get_timestamp')

    class Meta:
        model = FriendRequest
        fields = '__all__'

    def get_sender_profile(self, obj):
        if obj.sender:
            data = StudentData.objects.get(student=obj.sender)
            return data.profile.url

    def get_timestamp(self, obj):
        timestamp = obj.timestamp
        if timestamp:
            return timestamp.strftime("%H:%M:%S %d-%m-%Y")
        return ''
