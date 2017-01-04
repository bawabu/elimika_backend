import six


class PartialResponseMixin(object):

    def strip_fields(self, request, origi_fields):
        """
        Fetch a subset of fields from the serializer defined the
        ``fields`` query param.
        """
        if request is None or not hasattr(request, 'query_params'):
            return origi_fields

        if hasattr(request, 'method'):
            if request.method != 'GET':
                return origi_fields

        fields = request.query_params.get('fields', None)
        if isinstance(fields, six.string_types) and fields:
            fields = [f.strip() for f in fields.split(',')]

            return {
                field: origi_fields[field]
                for field in origi_fields if field in fields
            }

        return origi_fields
