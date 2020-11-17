from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    """Site user model. Inherit all from django default user model."""
    phone = models.CharField('电话', blank=True, max_length=11)
    qq = models.PositiveIntegerField('QQ', null=True, blank=True)
    wx_id = models.CharField('微信ID', max_length=20, null=True, blank=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'