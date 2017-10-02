from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.forms import PasswordInput
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from src.profiles.models import Profile

from src.gallery.helpers import log


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'is_active')
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            email=validated_data['email'],
            is_active=validated_data['is_active'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance = User(**validated_data)
        instance.save()
        return instance


class ProfileSerializer(ModelSerializer):
    """

    """
    # user = UserSerializer()
    # profile_picture = SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'id',
            'user',
            'profile_picture',
            'timestamp',
            'updated'
        ]
        read_only_fields = [
            'id', 'timestamp', 'updated', 'email'
        ]

    def get_profile_picture(self, obj):
        return obj.profile_picture.url

    def update(self, instance, validated_data):
        print("\n\n\nInside update\n\n\n")
        user = instance.user
        user.first_name = validated_data.get("first_name")
        user.last_name = validated_data.get("last_name")
        user.username = validated_data.get("username")
        user.email = validated_data.get("email")
        user.set_password(validated_data.get("password"))
        user.is_active = validated_data.get("is_active")
        user.save()
        instance.user = user
        instance.profile_picture = validated_data.get("profile_picture")
        instance.save()
        return instance


class CreateProfileSerializer(ModelSerializer):
    """

    """
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = [
            'user',
            'profile_picture',
        ]

    def create(self, validated_data):
        usr_data = validated_data['user']
        user = User.objects.create(**validated_data['user'])
        user.set_password(usr_data['password'])
        user.save()

        profile = Profile.objects.create(
            user=user,
            profile_picture=validated_data['profile_picture']
        )
        profile.save()
        return profile


class ProfileUpdateSerializer(ModelSerializer):
    """

    """
    user = UserSerializer(partial=True)

    class Meta:
        model = Profile
        fields = [
            "user",
            "profile_picture"
        ]
        # depth = 1
