from django.db import models

from listfield.fields import ListField


class TestModel(models.Model):
    list1 = ListField('LIST1', max_length=16)
    list2 = ListField(sep='.', max_length=16, blank=True)
    text1 = models.CharField(max_length=8, blank=True)
    text2 = models.CharField(max_length=8, blank=True)


class Father(models.Model):
    test_model = models.ForeignKey(
        'TestModel',
        on_delete=models.CASCADE
        )