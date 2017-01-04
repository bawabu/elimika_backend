# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import routers

from . import views

router = routers.SimpleRouter()

router.register(r'categories', views.CategoryViewSet)
router.register(r'knowledge', views.KnowledgeViewSet)
router.register(r'category_knowledge', views.CategoryKnowledgeViewSet)

urlpatterns = router.urls
