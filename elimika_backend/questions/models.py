# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.exceptions import ValidationError
from django.db import models

from elimika_backend.common.models.base import BaseModel
from elimika_backend.users.models import User, Learner
from elimika_backend.knowledge.models import Category


class Question(BaseModel):
    """
    Hold fields for questions to be asked.
    """

    question = models.TextField()
    tutor = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='tutor_questions')
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='category_questions')

    def __str__(self):
        """String representation."""
        return self.question


class Choice(BaseModel):
    """
    Hold choices for questions already present.
    """

    question = models.ForeignKey(
        Question, on_delete=models.PROTECT, related_name='question_choices')
    choice_text = models.CharField(max_length=255, blank=True)
    choice_image = models.ImageField(upload_to='choices/', blank=True)
    is_right = models.BooleanField(default=False)
    tutor = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='+')

    def __str__(self):
        """String representation."""
        return self.choice_text or self.choice_image

    def validate_choice_tutor(self):
        """
        The ``tutor`` that created the ``question`` should be the one to create
        its choice.
        """
        if self.tutor is not self.question.tutor:
            raise ValidationError({
                'tutor': (
                    'The tutor that created the referenced question should '
                    'be the one to create its choice.'
                )
            })

    def validate_choice_image(self):
        """
        Validate that either ``choice_image`` or ``choice_text`` is given
        as the choices.
        """
        if not self.choice_text and not self.choice_image:
            raise ValidationError(
                'Either a text or an image as choice is required.')

        if self.choice_text and self.choice_image:
            raise ValidationError(
                'Only a choice text or an image is required. Not both.')

    def validate_question_choices(self):
        """
        Validate that a question has choices of same type, i.e. either only
        ``choice_text`` or ``choice_image``
        """
        choice = self.question.question_choices.first()

        if choice:
            if choice.choice_text and self.choice_image:
                raise ValidationError({
                    'choice_image': (
                        'Previous choices for this question were text. '
                        'A choice of type text needs to be provided.'
                    )
                })

            if choice.choice_image and self.choice_text:
                raise ValidationError({
                    'choice_text': (
                        'Previous choices for this question were images. '
                        'A choice of type image needs to be provided.'
                    )
                })

    def clean(self, *args, **kwargs):
        """Override clean method."""
        self.validate_choice_tutor()
        self.validate_choice_image()
        self.validate_question_choices()
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
