from django.contrib.auth.models import AnonymousUser

from rest_framework import serializers

from elimika_backend.common.serializers.mixins import PartialResponseMixin


class AuditFieldsMixin(PartialResponseMixin, serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        exclude_fields = [
            'created', 'updated', 'created_by', 'updated_by'
        ]
        context = getattr(self, 'context', {})
        request = context.get('request', {})
        request_method = getattr(request, 'method', '').lower()
        include_in_methods = ['get', 'head', 'options']

        if request_method not in include_in_methods:
            for i in exclude_fields:
                if i in self.fields:
                    self.fields.pop(i)

    def _populate_audit_fields(self, data, create=False):
        request = self.context['request']
        user = request.user

        if not isinstance(user, AnonymousUser):
            data['updated_by'] = user

            if create:
                data['created_by'] = user

        return data

    def create(self, validate_data):
        self._populate_audit_fields(validate_data, True)
        return super().create(validate_data)

    def update(self, instance, validate_data):
        self._populate_audit_fields(validate_data)
        return super().update(instance, validate_data)

    def get_fields(self):
        origi_fields = super().get_fields()
        request = self.context.get('request', None)
        return self.strip_fields(request, origi_fields)
