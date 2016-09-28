# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework.serializers import ModelSerializer

from .models import Question, Choice, Answer


class ChoiceSerializer(ModelSerializer):

    class Meta:

        model = Choice


class QuestionSerializer(ModelSerializer):

    question_choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:

        model = Question



class AnswerSerializer(ModelSerializer):

    class Meta:

        model = Answer
