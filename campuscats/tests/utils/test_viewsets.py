from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured
from utils.viewsets import DispatchSerializerMixin


SERIALIZERS = {
    'retrieve_serializer': 'retrieve',
    'list_serializer': 'list',
    'create_serializer': 'create',
    'update_serializer': 'update',
    'partial_update_serializer': 'partial_update',
    }
    

class TestViewset(DispatchSerializerMixin, object):
    serializer_class = None


class DispatchSerializerMixinTestCase(TestCase):
    def test_dispatch(self):
        viewset = TestViewset()

        for k, v in SERIALIZERS.items():
            setattr(viewset, k, v)

        for action in SERIALIZERS.values():
            viewset.action = action
            serializer = viewset.get_serializer_class()
            self.assertEqual(action, serializer)

    def test_dispatch_list(self):
        viewset = TestViewset()
        viewset.write_serializer = 'write'

        WRITE_ACTIONS = ('create', 'update', 'partial_update')
        for action in WRITE_ACTIONS:
            viewset.action = action
            serializer = viewset.get_serializer_class()
            self.assertEqual('write', serializer)

    def test_dispatch_fallback(self):
        viewset = TestViewset()
        viewset.serializer_class = 'fallback'

        for action in SERIALIZERS.values():
            viewset.action = action
            serializer = viewset.get_serializer_class()
            self.assertEqual('fallback', serializer)

    def test_dispatch_error(self):
        viewset = TestViewset()
        viewset.action = 'unknow'

        self.assertRaisesMessage(
            ImproperlyConfigured, 
            "`TestViewset` has neither a "
            "serializer for action `unknow`, nor a fallback.",
            viewset.get_serializer_class
            )