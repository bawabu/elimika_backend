# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import serializers

from elimika_backend.common.serializers.base import AuditFieldsMixin
from elimika_backend.users.serializers import UserSerializer
from .models import Question, Choice, Answer


class ChoiceSerializer(AuditFieldsMixin):

    class Meta:

        model = Choice


class QuestionSerializer(AuditFieldsMixin):

    question_choices = ChoiceSerializer(many=True, read_only=True)
    category_name = serializers.ReadOnlyField(
        source='category.category_name')

    class Meta:

        model = Question
        read_only_fields = ('tutor',)


class AnswerSerializer(AuditFieldsMixin):

    is_right_answer = serializers.ReadOnlyField()

    class Meta:

        model = Answer
