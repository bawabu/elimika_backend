# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth import update_session_auth_hash

from rest_framework import serializers

from .models import User, Learner


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:

        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'password', 'confirm_password', 'is_tutor', 'is_staff',
        )

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.username = validated_data.get(
            'username', instance.username)
        instance.email = validated_data.get('email', instance.email)

        instance.save()

        password = validated_data.get('password', None)
        confirm_password = validated_data.get('confirm_password', None)

        if password and confirm_password and password == confirm_password:
            instance.set_password(password)
            instance.save()

        update_session_auth_hash(self.context.get('request'), instance)

        return instance


class LearnerSerializer(serializers.ModelSerializer):

    performance = serializers.ReadOnlyField()
    total_questions = serializers.ReadOnlyField()

    class Meta:

        model = Learner
