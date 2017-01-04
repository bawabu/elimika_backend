import datetime
import random

import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from elimika_backend.users.models import Learner, User
from .models import Question, Answer


class BaseFactory(DjangoModelFactory):

    created_by = User.objects.get(pk=1)
    updated_by = User.objects.get(pk=1)

    class Meta:

        abstract = True


def wrong_answer(obj):
    wrong_answers = obj.question.question_choices.exclude(is_right=True)

    return random.choice(wrong_answers)


class CorrectTeethAnswers(BaseFactory):
    """
    Create correct answers of category teeth.

    - create 22
    """

    learner = factory.Iterator(Learner.objects.all())
    question = factory.Iterator(
        Question.objects.filter(category__category_name='teeth')
    )
    choice = factory.LazyAttribute(
        lambda o: o.question.question_choices.filter(is_right=True)[0]
    )

    class Meta:

        model = Answer


class WrongTeethAnswers(BaseFactory):
    """
    Create wrong answers of category teeth.

    - create 11
    """

    learner = factory.Iterator(Learner.objects.all())
    question = factory.Iterator(
        Question.objects.filter(category__category_name='teeth')
    )
    choice = factory.LazyAttribute(wrong_answer)

    class Meta:

        model = Answer


class CorrectTeethTypesAnswers(BaseFactory):
    """
    Create correct answers of category teeth types.

    - create 110
    """

    learner = factory.Iterator(Learner.objects.all())
    question = factory.Iterator(
        Question.objects.filter(category__category_name='teeth_types')
    )
    choice = factory.LazyAttribute(
        lambda o: o.question.question_choices.filter(is_right=True)[0]
    )

    class Meta:

        model = Answer


class WrongTeethTypesAnswers(BaseFactory):
    """
    Create wrong answers of category teeth types.

    - create 22
    """

    learner = factory.Iterator(Learner.objects.all())
    question = factory.Iterator(
        Question.objects.filter(category__category_name='teeth_types')
    )
    choice = factory.LazyAttribute(wrong_answer)

    class Meta:

        model = Answer


class CorrectTeethSetsAnswers(BaseFactory):
    """
    Create correct answers of category teeth sets.

    - create 55
    """

    learner = factory.Iterator(Learner.objects.all())
    question = factory.Iterator(
        Question.objects.filter(category__category_name='teeth_sets')
    )
    choice = factory.LazyAttribute(
        lambda o: o.question.question_choices.filter(is_right=True)[0]
    )

    class Meta:

        model = Answer


class WrongTeethSetsAnswers(BaseFactory):
    """
    Create wrong answers of category teeth sets.

    - create 11
    """

    learner = factory.Iterator(Learner.objects.all())
    question = factory.Iterator(
        Question.objects.filter(category__category_name='teeth_sets')
    )
    choice = factory.LazyAttribute(wrong_answer)

    class Meta:

        model = Answer
