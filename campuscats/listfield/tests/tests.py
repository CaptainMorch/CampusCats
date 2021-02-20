from django.test import TestCase, SimpleTestCase
from django.core.checks import Error
from django.db.models import Model, F, Value, Transform
from django.db.models.functions import Concat
from django.core.exceptions import ValidationError

from listfield.fields import ListField
from .models import TestModel, Father


# pylint: disable=no-member
class ListFieldCheckMethodsTestCase(SimpleTestCase):
    def char_err(self, field_name):
        return Error(
            "CharFields must define a 'max_length' attribute.",
            obj=self.model._meta.get_field(field_name),
            id='fields.E120'
        )

    def sep_err(self, field_name):
        return Error(
            'Separator must be a single non-alphabetic character',
            obj=self.model._meta.get_field(field_name),
        )

    def test_check_max_length_and_sep(self):
        class TestCheckModel(Model):
            missing_max_length = ListField()
            sep_not_single = ListField(max_length=16, sep=', ')
            sep_alphabetic = ListField(max_length=16, sep='a')
            mix = ListField(sep='S')
        
        self.model = TestCheckModel()

        expected_errors = [
            self.char_err('missing_max_length'),
            self.sep_err('sep_not_single'),
            self.sep_err('sep_alphabetic'),
            self.char_err('mix'),
            self.sep_err('mix'),
        ]
        errors = self.model.check()
        self.assertEqual(errors, expected_errors)


class ListFieldModelTestCase(TestCase):
    def test_base(self):
        # pylint: disable=no-member
        model = TestModel.objects.create(
            list1=list('list1'),
            list2=list('list2'),
            )
        self.assertEqual(model.list1, list('list1'))
        self.assertEqual(model.list2, list('list2'))
        self.assertEqual(model, TestModel.objects.get(list1=list('list1')))
        self.assertEqual(model, TestModel.objects.get(list2=list('list2')))

    def test_sep_in_strings(self):
        model = TestModel(
            list1=['a', 'b,', 'c'],
            )
        self.assertRaises(ValidationError, model.full_clean)
        
        model = TestModel(
            list2=['a', 'b.', 'c'],
            )
        self.assertRaises(ValidationError, model.full_clean)

    def test_empty_value(self):
        invalid_kwargs = [{}, {'list1': []}, {'list1': None}, {'list1': ''}]
        for kwargs in invalid_kwargs:
            self.assertRaises(
                ValidationError,
                TestModel(**kwargs).full_clean
                )

        m1 = TestModel.objects.create(list1=[''], list2=[])
        m2 = TestModel.objects.create(list1=[''], list2=None)
        m3 = TestModel.objects.create(list1=[''], list2='')
        m4 = TestModel.objects.create(list1=[''])

        self.assertCountEqual(
            TestModel.objects.filter(list2=''),
            [m1, m2, m3, m4])
        self.assertFalse(TestModel.objects.filter(list2=None).exists())


class ListFieldLookupsTestCase(TestCase):
    # pylint: disable=no-member
    def test_raw(self):
        m1 = TestModel.objects.create(
            list1=['str1', 'str2'],
            list2=[',,', '  ']
            )
        m2 = TestModel.objects.create(
            list1=['str11', 'str22'],
            list2=[',,,', ' ']
            )
        m3 = TestModel.objects.create(
            list1=['StR1', 'STR2'],
            list2=[]
        )
        m4 = TestModel.objects.create(
            list1=['ssstr111', 'tr2'],
            list2=['']
        )

        qs = TestModel.objects.all()
        self.assertEqual(qs.get(list1__lf_has='str1'), m1)
        self.assertEqual(qs.get(list2__lf_has=' '), m2)
        self.assertEqual(qs.get(list2__lf_has=''), m4)

        self.assertCountEqual(qs.filter(list1__lf_ihas='str1'), [m1, m3])
        self.assertCountEqual(qs.filter(list1__lf_ihas='STr2'), [m1, m3])

    def test_expression(self):
        m1 = TestModel.objects.create(
            list1=['test', 'est', 'tes'],
            text1='eST')
        m2 = TestModel.objects.create(
            list1=['es'],
            text1='es')
        m3 = TestModel.objects.create(
            list1=['test', 'est', 'tes'],
            text1='e')

        qs = TestModel.objects.all()
        self.assertEqual(qs.get(list1__lf_has=F('text1')), m2)
        self.assertEqual(
            qs.get(list1__lf_has=Concat(F('text1'), Value('st'))),
            m3)
        self.assertCountEqual(
            qs.filter(list1__lf_ihas=F('text1')),
            [m1, m2])
            
    def test_relation(self):
        m1 = TestModel.objects.create(
            list1=['test', 'est', 'tes'],
            text1='eST')
        f = Father.objects.create(test_model=m1)

        self.assertEqual(
            f,
            Father.objects.get(
                test_model__list1__lf_ihas=F('test_model__text1')),
            )

    def test_bilateral_transforms(self):
        class UpperCase(Transform):
            lookup_name = 'upper'
            function = 'UPPER'
            bilateral = True
        ListField.register_lookup(UpperCase)

        m1 = TestModel.objects.create(
            list1=['test', 'est', 'tes'],
            text1='eST')

        self.assertEqual(
            m1,
            TestModel.objects.get(
                list1__upper__lf_has=F('text1')),
            )