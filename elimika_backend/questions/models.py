# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.exceptions import ValidationError
from django.db import models

from elimika_backend.common.models.base import BaseModel
from elimika_backend.users.models import User, Learner


CATEGORY_CHOICES = (
    ('some_type', 'Some type'),
)


class Question(BaseModel):
    """
    Hold fields for questions to be asked.
    """

    question = models.TextField()
    tutor = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='tutor_questions')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=100)

    def __str__(self):
        """String representation."""
        return self.question


class Choice(BaseModel):
    """
    Hold choices for questions already present.
    """

    question = models.ForeignKey(
        Question, on_delete=models.PROTECT, related_name='question_choices')
    choice = models.CharField(max_length=255)
    is_right = models.BooleanField(default=False)
    tutor = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='+')

    def __str__(self):
        """String representation."""
        return self.choice

    def validate_choice_tutor(self):
        """
        The ``tutor`` that created the ``question`` should be the one to create
        its ``choice``.
        """
        if self.tutor is not self.question.tutor:
            raise ValidationError({
                'tutor': (
                    'The tutor that created the referenced question should '
                    'be the one to create its choice.'
                )
            })

    def clean(self, *args, **kwargs):
        """Override clean method."""
        self.validate_choice_tutor()
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Override save method."""
        self.full_clean()
        super().save(*args, **kwargs)


class Answer(BaseModel):
    """
    Holds answers for a particular question given by a learner.
    """

    question = models.ForeignKey(
        Question, on_delete=models.PROTECT, related_name='question_answers')
    choice = models.ForeignKey(
        Choice, on_delete=models.PROTECT, related_name='+')
    learner = models.ForeignKey(
        Learner, on_delete=models.PROTECT, related_name='learner_answers')

    def __str__(self):
        """String representation."""
        return str(self.choice)

    @property
    def is_right_answer(self):
        """
        Evaluate if answer provided is the right one.
        """
        return (self.choice in
                self.question.question_choices.filter(is_right=True))
