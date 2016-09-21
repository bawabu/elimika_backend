# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import uuid

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


GENDER_CHOICES = (
    ('boy', 'Boy'),
    ('girl', 'Girl'),
)


@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})


class Learner(models.Model):
    """Hold fields for a learner."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    age = models.PositiveSmallIntegerField(blank=True, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=50)
    joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String representation."""
        return self.name
