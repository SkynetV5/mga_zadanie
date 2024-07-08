from rest_framework import serializers
from .models import Task
from simple_history.utils import update_change_reason
from django.contrib.auth.models import User

class TaskSerializers(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('id',)


class TaskHistorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Task.history.model
        fields = '__all__'

class RegisterSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user