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
    """
    Класа која претвара инстанцу модела класе у JSON објекат;
    """
    class Meta:
        # о ком моделу је реч
        model = User

        # која поља ће се серијализовати
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'is_active',
        ]
        # означавање да се лозинка може само уписати, а не и исчитати
        extra_kwargs = {"password": {"write_only": True}}

        read_only_fields = [
            'id', 'timestamp', 'updated', 'email'
        ]

    def create(self, validated_data):
        """
        Метода која се позива при извршењу POST захтева;
        или експлицитно позивом perform_create;
        Пре креирања валидира податке
        :param   validated_data:
        :return: User
        """
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
        """
        Метода која се позива при извршењу PUT захтева,
        или експлицитно позивом perform_update;
        Пре ажурирања валидира податке.
        :param   instance:
        :param   validated_data:
        :return: User
        """

        # екстраховање свих података и креирање
        instance = User(**validated_data)
        instance.save()
        return instance


class ProfileSerializer(ModelSerializer):
    """
    Класа која претвара инстанцу модела класе у JSON објекат;
    Враћа само основне податке о Профилу
    """

    class Meta:
        model = Profile

        fields = [
            'id',
            'user',
            'profile_picture',
            # 'timestamp',
            # 'updated'
        ]

    # Репрезентација атрибута profile_picture само као локацију слике
    def get_profile_picture(self, obj):
        return obj.profile_picture.url


    def update(self, instance, validated_data):
        """
        Метода која се позива при извршењу PUT захтева,
        или експлицитно позивом perform_update;
        Пре ажурирања валидира податке.
        :param   instance:
        :param   validated_data:
        :return: Profile
        """
        user = instance.user
        user.first_name = validated_data.get("first_name", instance.user.first_name)
        user.last_name  = validated_data.get("last_name",  instance.user.last_name)
        user.username   = validated_data.get("username",   instance.user.username)
        user.email      = validated_data.get("email",      instance.user.email)
        user.is_active  = validated_data.get("is_active",  instance.user.is_active)

        password = validated_data.get("password", None)
        if password is not None:
            user.set_password(password)
        user.save()

        instance.user = user
        instance.profile_picture = validated_data.get("profile_picture", instance.profile_picture)
        instance.save()
        return instance


class CreateProfileSerializer(ModelSerializer):
    """
    Класа за серијализацију инстанце модела Профиле;
    Серијализује JSON објекат у инстанцу модела Профил
    """

    user = UserSerializer()

    class Meta:
        model = Profile
        fields = [
            'user',
            'profile_picture',
        ]

    def create(self, validated_data):
        """
        Метода која се позива при извршењу POST захтева,
        или експлицитно позивом perform_create;
        Пре ажурирања валидира податке.
        :param   instance:
        :param   validated_data:
        :return: Profile
        """

        usr_data = validated_data['user']
        user     = User.objects.create(**validated_data['user'])
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
    Класа за серијализацију инстанце модела Лајк,
    код ажурирања; Враћа све постојеће податке за модел Лајк
    """

    # омогућавање парцијалног ажурирања корисника
    user = UserSerializer(partial=True)

    class Meta:
        model = Profile

        fields = [
            'id',
            "user",
            "profile_picture"
        ]

        read_only_fields = [
            'id', 'timestamp', 'updated', 'email'
        ]