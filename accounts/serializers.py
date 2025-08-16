from rest_framework import serializers
from .models import UserModel


class RegisterAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['nickname', 'email', 'password']
