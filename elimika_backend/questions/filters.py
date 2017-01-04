# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import django_filters
from .models import Question, Choice, Answer


class QuestionFilter(django_filters.FilterSet):

    class Meta:

        model = Question


class ChoiceFilter(django_filters.FilterSet):

    class Meta:

        model = Choice


class AnswerFilter(django_filters.FilterSet):

    class Meta:

        model = Answer
