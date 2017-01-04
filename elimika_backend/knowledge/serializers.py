# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import serializers

from .models import Category, Knowledge


class CategorySerializer(serializers.ModelSerializer):

    parent_category = serializers.ReadOnlyField(
        source='category.category_name')

    class Meta:

        model = Category


class KnowledgeSerializer(serializers.ModelSerializer):

    category_name = serializers.ReadOnlyField(
        source='category.category_name')

    class Meta:

        model = Knowledge
