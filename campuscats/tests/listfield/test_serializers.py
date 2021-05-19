from django.test import TestCase

from rest_framework.serializers import ValidationError, ModelSerializer

from utils.test import AssertSerializerValidationMixin
from listfield.serializers import AllowListFieldMixin
from .models import TestModel


class TestModelSerializer(AllowListFieldMixin, ModelSerializer):
    class Meta:
        model = TestModel
        fields = '__all__'


class ListFieldSerializerTestCase(AssertSerializerValidationMixin, TestCase):
    def test_base(self):
        data = {
            'list1': list('list1'),
            'list2': list('list2'),
            'text1': 'text1',
        }
        m = TestModel.objects.create(**data)

        serialized = TestModelSerializer(m).data

        serialized.pop('id')
        data['text2'] = ''
        self.assertDictEqual(serialized, data)

        deserializer = TestModelSerializer(data=serialized)
        self.assertTrue(deserializer.is_valid())
        self.assertEqual(data, deserializer.validated_data)
        deserialized = deserializer.save()
        self.assertEqual(m.list1, deserialized.list1)
        self.assertEqual(m.list2, deserialized.list2)

    def test_validation_max_length(self):
        deserializer = TestModelSerializer(data={
            'list1': ['exactly', '17chars'],
            'list2': ['exactly16chars'],
            })
        self.assertFalse(deserializer.is_valid())
        self.assertValidationErrorCodes(
            deserializer.errors,
            {'list1': 'max_length'}
            )

    def test_validation_no_sep(self):
        deserializer = TestModelSerializer(data={
            'list1': ['has', 'sep,', 'in'],
            'list2': ['.'],
            })
        self.assertFalse(deserializer.is_valid())
        self.assertValidationErrorCodes(
            deserializer.errors,
            {'list1': 'no_sep', 'list2': 'no_sep'}
        )

    def test_validation_type(self):
        deserializer = TestModelSerializer(data={
            'list1': 'not-a-list',
            'list2': ['not-string', 1],
            })
        self.assertFalse(deserializer.is_valid())
        self.assertValidationErrorCodes(
            deserializer.errors,
            {'list1': 'not_list', 'list2': 'invalid'}
        )

    def test_validation_empty(self):
        l1, l2 = 'list1', 'list2'
        cases = [
            ({l1: '', l2: ''}, {l1: 'not_list', l2: 'not_list'}),
            ({l1: None, l2: None}, {l1: 'null', l2: 'null'}),
            ({l1: [], l2: []}, {l1: 'blank'}),
            ({}, {l1: 'required'})
        ]
        for data, expected_errors in cases:
            with self.subTest(data=str(data)):
                deserializer = TestModelSerializer(data=data)
                self.assertFalse(deserializer.is_valid())
                self.assertValidationErrorCodes(
                    deserializer.errors,
                    expected_errors
                )