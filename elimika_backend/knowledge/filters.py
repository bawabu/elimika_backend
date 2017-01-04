# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import django_filters
from .models import Category, Knowledge


class CategoryFilter(django_filters.FilterSet):

    class Meta:

        model = Category


class KnowledgeFilter(django_filters.FilterSet):

    class Meta:

        model = Knowledge
