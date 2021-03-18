from django.db.models import CharField, Field
from django.core import checks
from django.core.exceptions import ValidationError

from .forms import ListFieldFormField


# https://docs.djangoproject.com/en/3.1/howto/custom-model-fields/
# https://docs.djangoproject.com/en/3.1/ref/models/fields/#field-api-reference
# https://github.com/django/django/blob/master/django/db/models/fields/__init__.py
# https://github.com/fle/django-multi-email-field/blob/master/multi_email_field/fields.py
class ListField(CharField):
    description = 'List of strings'

    def __init__(self, *args, sep=',', **kwargs):
        self.sep = sep
        super().__init__(*args, **kwargs)

    def check(self, **kwargs):
        return [
            *super().check(**kwargs),
            *self._check_separator(),
        ]

    def _check_separator(self):
        if not (isinstance(self.sep, str)
                and len(self.sep) == 1
                and not self.sep.isalpha()):
            return [
                checks.Error(
                    'Separator must be a single non-alphabetic character',
                    obj=self,
                )
            ]
        return []

    def to_python(self, value):
        # None, empty string, empty list
        if not value:
            return []
        if isinstance(value, list):
            if any(self.sep in s for s in value):
                raise ValidationError(
                    'strings to store must not contain seprater')
            return value
        # value must be a string now
        if not value.startswith(self.sep) or not value.endswith(self.sep):
            raise ValidationError('value should be wrapped by seprater')
        strings = value.split(self.sep)
        return strings[1:-1]

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def get_internal_type(self):
        return "CharField"

    def get_prep_value(self, value):
        # this method may also be called on lookup values,
        # so we'd better return value itself as possible as we can
        if value == [] or value == ():
            return ''
        if not value:
            return value
        if isinstance(value, list) or isinstance(value, tuple):
            return '{sep}{strings}{sep}'.format(
                sep=self.sep,
                strings=self.sep.join(value)
                )
        # https://docs.djangoproject.com/en/3.1/howto/custom-model-fields/#converting-python-objects-to-query-values
        return str(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        # always store None as empty string instead of null
        if not value:
            return ''
        return self.get_prep_value(value)

    def formfield(self, **kwargs):
        defaults = {'sep': self.sep, 'form_class': ListFieldFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        # Only include 'sep' if it's not the default
        if self.sep != ",":
            kwargs['sep'] = self.sep
        return name, path, args, kwargs