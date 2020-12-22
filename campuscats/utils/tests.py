from django.test import TestCase
from . import create_choices_class


class CreateChoicesClassTests(TestCase):
    choices = [('TEST1', 'test1'), ('TEST2', 'test2'), ('TEST3', 'test3')]
    result = [(1, 'test1'), (2, 'test2'), (3, 'test3')]

    def test_normal(self):
        Klass = create_choices_class('Klass', *self.choices)
        self.assertEqual(Klass.choices, self.result)

    def test_use_bool(self):
        choices = self.choices[:-1]
        Klass = create_choices_class('Klass', *choices)
        self.assertEqual(Klass.choices, [(0, 'test1'), (1, 'test2')])

    def test_empty(self):
        Klass = create_choices_class('Klass', *self.choices, null=True)
        self.assertEqual(Klass.choices, [(None, '未知')] + self.result)

    def test_empty_label(self):
        Klass = create_choices_class('Klass', *self.choices, null=True, null_label='t')
        self.assertEqual(Klass.choices, [(None, 't')] + self.result)