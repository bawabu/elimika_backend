# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from collections import defaultdict

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import filters

from .models import Category, Knowledge
from .serializers import CategorySerializer, KnowledgeSerializer
from .filters import CategoryFilter, KnowledgeFilter


class CategoryViewSet(ReadOnlyModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = CategoryFilter


class KnowledgeViewSet(ReadOnlyModelViewSet):

    queryset = Knowledge.objects.all()
    serializer_class = KnowledgeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = KnowledgeFilter


class CategoryKnowledgeViewSet(KnowledgeViewSet):

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        data = response.data
        results = defaultdict(list)

        for item in data:
            knowledge = {
                'id': item['id'],
                'text': item['text'],
                'image': item['image']
            }
            category = item['category_name']
            results[category].append(knowledge)

        response.data = [
            {
                'category': k,
                'knowledge': v
            } for k, v in results.items()
        ]

        return response
