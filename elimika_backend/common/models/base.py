import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    """
    Contains fields present in all models.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='+',
        blank=True, null=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='+',
        blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)

    class Meta():
        """Meta class for ``BaseModel``."""
        ordering = ('-updated', '-created',)
        abstract = True

    def validate_updated_greater_than_created_date(self):
        """
        Validate that the ``updated`` field is greater than the ``created``
        field.
        """
        if self.updated < self.created:
            raise ValidationError({
                'updated': (
                    'The updated date cannot be in the past of created '
                    'date.'
                )
            })

    def preserve_created_by(self):
        """
        Ensures that ``created_by`` field is not overriden.
        """
        try:
            original = self.__class__.objects.get(pk=self.pk)
            self.created_by = original.created_by
        except self.__class__.DoesNotExist:
            pass

    def save(self, *args, **kwargs):
        """Override save method."""
        self.preserve_created_by()
        self.full_clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Override delete method."""
        self.deleted = True
        self.save(*args, **kwargs)
