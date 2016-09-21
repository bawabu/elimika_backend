# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework.serializers import ModelSerializer

from .models import Question, Choice, Answer


class QuestionSerializer(ModelSerializer):

    class Meta:

        model = Question


class ChoiceSerializer(ModelSerializer):

    class Meta:

        model = Choice


class AnswerSerializer(ModelSerializer):

    class Meta:

        model = Answer
