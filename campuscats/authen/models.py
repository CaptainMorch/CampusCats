from django.db import models
from django.contrib.auth.models import AbstractUser
from utils import create_choices_class
from . import permissions


class User(AbstractUser):
    """Project user model."""
    # leave blank for future extension
    # https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
    pass


class Contact(models.Model):
    """model for user contact info"""
    Permissions = create_choices_class(
        'Permissions',
        ('MEMBERSONLY', '仅成员'),
        ('VERIFIED', '成员及校邮验证用户'),
        ('TRUSTED','所有受信任访客'),
        ('ALLOWANY', '任何人'),
        )

    user = models.ForeignKey(
        User,
        verbose_name='用户',
        related_name='contacts',
        related_query_name='contact',
        on_delete=models.CASCADE,
    )
    name = models.CharField('方式', max_length=16)
    permission = models.PositiveSmallIntegerField(
        '对谁可见',
        choices=Permissions.choices,
        default=Permissions.TRUSTED)
    value = models.CharField('值', max_length=32, blank=True)
    qr_code = models.ImageField(
        '二维码',
        null=True, blank=True,
        upload_to='user/qrcode/')
    
    class Meta:
        verbose_name = '联系方式'
        verbose_name_plural = '联系方式'

    def __str__(self):
        return f'{self.user!s}-{self.name}'

    def get_permission_class(self):
        """get the drf permission class required for viewing this contact"""
        PERMISSION_MAP = {
            'MEMBERSONLY': permissions.MemebersOnly,
            'VERIFIED': permissions.TrustByEmail,
            'TRUSTED': permissions.TrustByEmailNetworkGroup,
            'ALLOWANY': permissions.AllowAny,
        }
        name = self.permission.name
        return PERMISSION_MAP[name]