# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import uuid
import math

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


GENDER_CHOICES = (
    ('boy', 'Boy'),
    ('girl', 'Girl'),
)


@python_2_unicode_compatible
class User(AbstractUser):

    is_tutor = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})


class Learner(models.Model):
    """Hold fields for a learner."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    age = models.PositiveSmallIntegerField(blank=True, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=50)
    joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String representation."""
        return self.name

    @property
    def performance(self):
        """Performance in percentage per category."""
        t_right = self.learner_answers.filter(
            question__category__category_name='teeth',
            choice__is_right=True).count()
        t_total = self.learner_answers.filter(
            question__category__category_name='teeth').count()

        try:
            t_percent = math.ceil(t_right / t_total * 100)
        except ZeroDivisionError:
            t_percent = 0

        tt_right = self.learner_answers.filter(
            question__category__category_name='teeth_types',
            choice__is_right=True).count()
        tt_total = self.learner_answers.filter(
            question__category__category_name='teeth_types').count()

        try:
            tt_percent = math.ceil(tt_right / tt_total * 100)
        except ZeroDivisionError:
            tt_percent = 0

        ts_right = self.learner_answers.filter(
            question__category__category_name='teeth_sets',
            choice__is_right=True).count()
        ts_total = self.learner_answers.filter(
            question__category__category_name='teeth_sets').count()

        try:
            ts_percent = math.ceil(ts_right / ts_total * 100)
        except ZeroDivisionError:
            ts_percent = 0

        return [t_percent, tt_percent, ts_percent]

    @property
    def total_questions(self):
        """Return total questions answered per category"""
        from elimika_backend.questions.models import Question

        t_answeredQ = self.learner_answers.filter(
            question__category__category_name='teeth').order_by(
            'question__id').distinct('question__id').count()
        t_total = Question.objects.filter(category__category_name='teeth').count()
        tt_answeredQ = self.learner_answers.filter(
            question__category__category_name='teeth_types').order_by(
            'question__id').distinct('question__id').count()
        tt_total = Question.objects.filter(
            category__category_name='teeth_types').count()
        ts_answeredQ = self.learner_answers.filter(
            question__category__category_name='teeth_sets').order_by(
            'question__id').distinct('question__id').count()
        ts_total = Question.objects.filter(
            category__category_name='teeth_sets').count()

        return [
            { 'answered': t_answeredQ, 'total': t_total },
            { 'answered': tt_answeredQ, 'total': tt_total },
            { 'answered': ts_answeredQ, 'total': ts_total }
        ]
