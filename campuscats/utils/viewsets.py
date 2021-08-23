from django.core.exceptions import ImproperlyConfigured


class DispatchSerializerMixin:
    """Choose different serializer class based on actions
    
    property:
        serializer_mapping
        retrieve_serializer
        list_serializer
        write_serializer
        create_serializer
        update_serializer
        partial_update_serializer

    method:
        get_serializer_class
        get_fallback_serializer_class
        get_serializer_mapping
    """

    serializer_mapping = {
        'retrieve': ('retrieve_serializer',),
        'list': ('list_serializer',),
        'create': ('create_serializer', 'write_serializer'),
        'update': ('update_serializer', 'write_serializer'),
        'partial_update': ('partial_update_serializer', 'write_serializer'),
    }
    retrieve_serializer = None
    list_serializer = None
    write_serializer = None
    create_serializer = None
    update_serializer = None
    partial_update_serializer = None

    def get_serializer_mapping(self):
        return self.serializer_mapping
        
    def get_fallback_serializer_class(self):
        return self.serializer_class
        
    def get_serializer_class(self):
        action = self.action
        mapping = self.get_serializer_mapping()

        serializers = mapping.get(action, tuple())
        for serializer in serializers:
            serializer = getattr(self, serializer, None)
            if serializer is not None:
                return serializer

        fallback = self.get_fallback_serializer_class()
        if fallback is not None:
            return fallback
        
        raise ImproperlyConfigured(
            f"`{self.__class__.__name__}` has neither a "
            f"serializer for action `{action}`, nor a fallback."
        )