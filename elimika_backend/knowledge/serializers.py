# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework.serializers import ModelSerializer

from .models import Category, Knowledge


class CategorySerializer(ModelSerializer):

    class Meta:

        model = Category


class KnowledgeSerializer(ModelSerializer):

    class Meta:

        model = Knowledge
