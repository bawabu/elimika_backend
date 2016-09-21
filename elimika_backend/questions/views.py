# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework.viewsets import ModelViewSet

from .models import Question, Choice, Answer
from .serializers import (QuestionSerializer, ChoiceSerializer,
                          AnswerSerializer)


class QuestionViewSet(ModelViewSet):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class ChoiceViewSet(ModelViewSet):

    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


class AnswerViewSet(ModelViewSet):

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
