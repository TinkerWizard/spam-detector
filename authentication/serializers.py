from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import AllUsers


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = AllUsers
        fields = ['name', 'phone', 'email', 'password']

    def create(self, validated_data):
        user = AllUsers.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(phone=data['phone'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return user
    