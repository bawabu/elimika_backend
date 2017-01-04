# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from collections import defaultdict
from itertools import groupby
import dateutil.parser

from sklearn import tree

from django.db import transaction
from django.db.models import Count, Sum, Case, When, IntegerField, Q

from rest_framework.viewsets import ModelViewSet
from rest_framework import filters, permissions, status
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from elimika_backend.users.models import Learner

from .models import Question, Choice, Answer
from .serializers import (QuestionSerializer, ChoiceSerializer,
                          AnswerSerializer)
from .filters import (
    QuestionFilter, ChoiceFilter, AnswerFilter)


def predict_category(learner):
    """
    Predict category that a learner is most likely to fail.
    """
    learners = Answer.objects.exclude(learner=learner.pk).annotate(
        age_group=Case(
            When(learner__age__lte=6, then=0),
            When(learner__age__gte=10, then=2),
            default=1, output_field=IntegerField()
        ),
        gender_group=Case(
            When(learner__gender='boy', then=0),
            default=1, output_field=IntegerField()
        )
    ).distinct('learner').order_by('learner').values_list(
        'age_group', 'gender_group')

    failed_teeth = Learner.objects.exclude(pk=learner.pk).filter(
        learner_answers__question__category__category_name='teeth'
    ).annotate(
        failed_answers=Sum(Case(
            When(learner_answers__choice__is_right=False, then=1),
            default=0, output_field=IntegerField()
        ))
    ).order_by('id').values_list('failed_answers')
    failed_teeth_types = Learner.objects.exclude(pk=learner.pk).filter(
        learner_answers__question__category__category_name='teeth_types'
    ).annotate(
        failed_answers=Sum(Case(
            When(learner_answers__choice__is_right=False, then=1),
            default=0, output_field=IntegerField()
        ))
    ).order_by('id').values_list('failed_answers')
    failed_teeth_sets = Learner.objects.exclude(pk=learner.pk).filter(
        learner_answers__question__category__category_name='teeth_sets'
    ).annotate(
        failed_answers=Sum(Case(
            When(learner_answers__choice__is_right=False, then=1),
            default=0, output_field=IntegerField()
        ))
    ).order_by('id').values_list('failed_answers')

    # teeth: 0, teeth_types: 1, teeth_sets: 2
    most_failed_category = []
    for i in range(learners.count()):
        max_cat = max(
            failed_teeth[i], failed_teeth_types[i], failed_teeth_sets[i]
        )

        if failed_teeth_types[i] == max_cat:
            most_failed_category.append(1)
        else:
            if failed_teeth_sets[i] == max_cat:
                most_failed_category.append(2)
            else:
                most_failed_category.append(0)

    classifier = tree.DecisionTreeClassifier().fit(
        learners, most_failed_category)

    if learner.age <= 6:
        learner_age = 0
    elif learner.age >= 10:
        learner_age = 2
    else:
        learner_age = 1

    learner_gender = 0 if learner.gender == 'boy' else 1

    predicted_cat = classifier.predict([(learner_age, learner_gender)])

    return predicted_cat[0]


class QuestionViewSet(ModelViewSet):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = QuestionFilter

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)

        return (permissions.IsAuthenticated(),)

    @list_route(methods=['post'])
    @transaction.atomic
    def create_question_choices(self, request):
        context = {'request': request}
        data = request.data

        q_serializer = QuestionSerializer(data=data, context=context)
        q_serializer.is_valid(raise_exception=True)
        question = q_serializer.save(tutor=self.request.user)

        for i in range(4):
            choice_data = {
                'choice_text': data.get('choices[' + str(i) + '][choice_text]', ''),
                'is_right': data.get('choices[' + str(i) + '][is_right]', ''),
                'question': question.pk,
                'tutor': self.request.user.pk
            }
            c_serializer = ChoiceSerializer(data=choice_data, context=context)
            c_serializer.is_valid(raise_exception=True)
            c_serializer.save(tutor=self.request.user, question=question)

        return Response(q_serializer.data, status=status.HTTP_201_CREATED)

    @detail_route(methods=['get', 'patch'])
    @transaction.atomic
    def update_question_choices(self, request, pk=None, *args, **kwargs):
        pass

    @detail_route(methods=['get'])
    def best_questions(self, request, pk=None, *args, **kwargs):
        """
        Return the ``best`` questions for a given user.

        Qualifications for a 'best' question:
            - Not answered by the learner (new questions)
            - Failed by many learners including themselves
        """
        response = self.list(request, *args, **kwargs)

        if not pk:
            # raise error
            pass

        try:
            learner = Learner.objects.get(pk=pk)
        except Learner.DoesNotExist:
            pass

        prediction = predict_category(learner)

        teeth_no, teeth_types_no, teeth_sets_no = 3, 5, 3
        if prediction == 0:
            teeth_no = 5
        if prediction == 1:
            teeth_types_no = 7
        if prediction == 2:
            teeth_sets_no = 5

        new_questions = Question.objects.exclude(
            question_answers__learner=learner
        ).order_by('id').distinct('id')

        old_questions = Question.objects.filter(
            question_answers__learner=learner
        ).order_by('id').distinct('id')

        t_cat = new_questions.filter(category__category_name='teeth').count()
        tt_cat = new_questions.filter(category__category_name='teeth_types').count()
        ts_cat = new_questions.filter(category__category_name='teeth_sets').count()

        if t_cat < teeth_no:
            reminder = teeth_no - t_cat
            extra = old_questions.filter(category__category_name='teeth')[:reminder]
            new_questions = new_questions | extra

        if tt_cat < teeth_types_no:
            reminder = teeth_types_no - tt_cat
            extra = old_questions.filter(category__category_name='teeth_types')[:reminder]
            new_questions = new_questions | extra

        if ts_cat < teeth_sets_no:
            reminder = teeth_sets_no - ts_cat
            extra = old_questions.filter(category__category_name='teeth_sets')[:reminder]
            new_questions = new_questions | extra

        serializer = self.get_serializer(new_questions, many=True)
        data = serializer.data
        results = defaultdict(list)

        for item in data:
            questions = {
                'id': item['id'],
                'question': item['question'],
                'category': item['category_name'],
                'question_image': item['question_image'],
                'question_choices': item['question_choices']
            }
            category = item['category_name']
            results[category].append(questions)

        best_questions = []
        for k, v in results.items():
            if k == 'teeth':
                v = v[:teeth_no]
            elif k == 'teeth_types':
                v = v[:teeth_types_no]
            else:
                v = v[:teeth_sets_no]

            best_questions.append({
                'category': k,
                'questions': v
            })

        response.data = best_questions

        return response


class CategoryQuestionsViewSet(QuestionViewSet):

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        data = response.data
        results = defaultdict(list)

        for item in data:
            questions = {
                'id': item['id'],
                'question': item['question'],
                'category': item['category_name'],
                'question_image': item['question_image'],
                'question_choices': item['question_choices']
            }
            category = item['category_name']
            results[category].append(questions)

        response.data = [
            {
                'category': k,
                'questions': v
            } for k, v in results.items()
        ]

        return response


class ChoiceViewSet(ModelViewSet):

    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ChoiceFilter


class AnswerViewSet(ModelViewSet):

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = AnswerFilter

    @list_route(methods=['get'])
    def answer_stats(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)

        teeth_answers = Answer.objects.filter(
            question__category__category_name='teeth'
        ).count()
        right_teeth = Answer.objects.filter(
            question__category__category_name='teeth',
            choice__is_right=True
        ).count()

        teeth_types_answers = Answer.objects.filter(
            question__category__category_name='teeth_types'
        ).count()
        right_teeth_types = Answer.objects.filter(
            question__category__category_name='teeth_types',
            choice__is_right=True
        ).count()

        teeth_sets_answers = Answer.objects.filter(
            question__category__category_name='teeth_sets'
        ).count()
        right_teeth_sets = Answer.objects.filter(
            question__category__category_name='teeth_sets',
            choice__is_right=True
        ).count()

        response.data = {
            'total_answers': teeth_answers + teeth_types_answers + teeth_sets_answers,
            'teeth': {
                'total': teeth_answers,
                'right': '{0:.0f}'.format(right_teeth / teeth_answers * 100),
                'wrong': '{0:.0f}'.format(
                    (teeth_answers - right_teeth) / teeth_answers * 100
                )
            },
            'teeth_types': {
                'total': teeth_types_answers,
                'right': '{0:.0f}'.format(
                    right_teeth_types / teeth_types_answers * 100),
                'wrong': '{0:.0f}'.format(
                    (teeth_types_answers - right_teeth_types) / teeth_types_answers * 100
                )
            },
            'teeth_sets': {
                'total': teeth_sets_answers,
                'right': '{0:.0f}'.format(right_teeth_sets / teeth_sets_answers * 100),
                'wrong': '{0:.0f}'.format(
                    (teeth_sets_answers - right_teeth_sets) / teeth_sets_answers * 100
                )
            }
        }

        return response


class DailyAnswersViewSet(AnswerViewSet):

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        data = response.data
        stats = []
        daily_answers = []

        for item in data:
            created = dateutil.parser.parse(item['created'])
            tmp = (item['id'], created)
            stats.append(tmp)

        for key, values in groupby(stats, key=lambda stat: stat[1].date()):
            answers = {
                'date': str(key),
                'total_answers': len(list(values))
            }
            daily_answers.append(answers)

        response.data = daily_answers

        return response


class StatisticsViewSet(AnswerViewSet):

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        total_learners = Learner.objects.all().count()
        total_questions = Question.objects.all().count()
        total_answers = Answer.objects.all().count()

        response.data = {
            'learners': total_learners,
            'questions': total_questions,
            'answers': total_answers
        }

        return response
