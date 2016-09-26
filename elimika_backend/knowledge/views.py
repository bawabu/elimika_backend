# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework.viewsets import ReadOnlyModelViewSet 

from .models import Category, Knowledge
from .serializers import CategorySerializer, KnowledgeSerializer


class CategoryViewSet(ReadOnlyModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class KnowledgeViewSet(ReadOnlyModelViewSet):

    queryset = Knowledge.objects.all()
    serializer_class = KnowledgeSerializer
