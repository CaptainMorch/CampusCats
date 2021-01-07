from django.apps import AppConfig

from listfield.fields import ListField
from listfield.lookups import Has, IHas


class ListFieldConfig(AppConfig):
    name = 'listfield'

    def ready(self):
        ListField.register_lookup(Has)
        ListField.register_lookup(IHas)