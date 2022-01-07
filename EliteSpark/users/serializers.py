from rest_framework import serializers
from .models import StudentData


class StudentDataSerilizer(serializers.ModelSerializer):

    class Meta:
        model = StudentData
        fields = '__all__'


