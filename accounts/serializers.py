from rest_framework import serializers
from .models import UserModel
import re


class RegisterAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['nickname', 'email', 'password']

    def validate_email(self, value):
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', value):
            raise serializers.ValidationError("Invalid email format")
        return value.lower()


class LoginAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    class Meta:
        fields = ['email', 'password']

    def validate_email(self, value):
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', value):
            raise serializers.ValidationError("Invalid email format")
        return value.lower()
