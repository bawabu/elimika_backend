# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import routers

from . import views

router = routers.SimpleRouter()

router.register(r'questions', views.QuestionViewSet)
router.register(r'choices', views.ChoiceViewSet)
router.register(r'answers', views.AnswerViewSet)

urlpatterns = router.urls
