# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import uuid

from django.core.exceptions import ValidationError
from django.db import models


class Category(models.Model):
    """
    Hold the various categories of the knowledge(science) to be stored.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(
        'self', related_name='child_categories', blank=True, null=True,
        on_delete=models.PROTECT)
    category_name = models.CharField(max_length=255)
    base_category = models.BooleanField(default=True)

    def __str__(self):
        """String representation."""
        return self.category_name

    def validate_base_category(self):
        """
        Validate that if ``base_category`` is True that ``category``
        (parent category) is not provided. If ``base_category`` is False then
        ``category`` must be provided.
        """
        if self.base_category is True and self.category:
            raise ValidationError({
                'category': (
                    'A category cannot be the base category if the parent '
                    'category is provided.'
                )
            })

        if self.base_category is False and not self.category:
            raise ValidationError({
                'category': (
                    'A category that is not the base category needs to '
                    'specify the parent category.'
                )
            })

    def clean(self, *args, **kwargs):
        """Override clean method."""
        self.validate_base_category()
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Override save method."""
        self.full_clean()
        super().save(*args, **kwargs)


def img_directory_path(instance, filename):
    """
    Method to return the custom filepath for each image uploaded in
    ``Knowledge``.
    """
    return '{0}/{1}'.format(str(instance.category), filename)


class Knowledge(models.Model):
    """
    Hold the knowledge for standard 4 science.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(
        Category, related_name='category_knowledges', on_delete=models.PROTECT)
    text = models.TextField()
    image = models.ImageField(upload_to=img_directory_path, blank=True)

    def __str__(self):
        """String representation."""
        return '{0}: {1}'.format(str(self.category), self.text)
