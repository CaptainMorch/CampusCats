from rest_framework.serializers import Field, ValidationError

from listfield import fields


# https://github.com/encode/django-rest-framework/blob/75edc4f0ecbfc8a1d416ac1e1eb0ea1fe70f06a4/rest_framework/fields.py#L754
# We need the primitive datatype to be 'list', so subclassing 
#   CharField is impossible, though we'd like to.
class ListField(Field):
    default_error_messages = {
        'not_list': 'Must provide a list.',
        'invalid': 'Values must be all string.',
        'no_sep': "Values can not contain separator '{sep}'.",
        'blank': 'This field may not be blank.',
        'max_length': 'This field must has no more than {max_length} characters.'
    }

    def __init__(self, **kwargs):
        self.sep = kwargs.pop('sep')
        self.max_length = kwargs.pop('max_length')
        self.allow_blank = kwargs.pop('allow_blank', False)
        super().__init__(**kwargs)

    def _validate(self, data):
        LEADING_AND_TRAILING = 2
        if not isinstance(data, list):
            self.fail('not_list')
        if not data and not self.allow_blank:
            self.fail('blank')
        if not all(isinstance(s, str) for s in data):
            self.fail('invalid')
        if any(self.sep in s for s in data):
            self.fail('no_sep', sep=self.sep)
        joined_length = len(' '.join(data)) + LEADING_AND_TRAILING
        if joined_length > self.max_length:
            self.fail('max_length', max_length=self.max_length)

    def to_internal_value(self, data):
        self._validate(data)
        return data

    def to_representation(self, value):
        return value

        
class AllowListFieldMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.serializer_field_mapping[fields.ListField] = ListField
         
    def build_standard_field(self, field_name, model_field):
        field_class, field_kwargs = super().build_standard_field(
            field_name, model_field)

        if issubclass(field_class, ListField):
            field_kwargs['sep'] = model_field.sep
            # we are not a subclass of serializers.CharField, so
            # 'allow_blank' won't be automatically set for us
            field_kwargs['allow_blank'] = model_field.blank
        return field_class, field_kwargs