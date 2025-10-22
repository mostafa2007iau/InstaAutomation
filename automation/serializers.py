from rest_framework import serializers
from .models import InstagramAccount, MonitoredPost, AutomationRule, TaskLog
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class InstagramAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramAccount
        fields = '__all__'

class MonitoredPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoredPost
        fields = '__all__'

class AutomationRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutomationRule
        fields = '__all__'
        read_only_fields = ('post',)

class TaskLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskLog
        fields = '__all__'