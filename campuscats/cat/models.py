from django.db import models
from django.conf import settings

from utils import create_choices_class

# Create your models here.
class Cat(models.Model):
    """猫猫的数据库主表，用于存储需要经常查找的 column"""
    
    Gender = create_choices_class(
        'Gender',
        ('BOY', '男孩子'), ('GIRL', '女孩子'),
        null=True,
        )

    Fur = create_choices_class(
        'Fur',
        ('LONG', '长毛'), ('SHORT', '短毛'),
        null=True,
        )

    CatType = create_choices_class(
        'CatType',
        ('WHITE', '白猫'),
        ('BLACK', '黑猫'),
        ('BLACK_W', '奶牛猫'),
        ('LIHUA', '狸花猫'),
        ('LIHUA_W', '狸白'),
        ('ORANGE', '橘猫'),
        ('ORANGE_W', '橘白'),
        ('SANHUA', '三花猫'),
        ('DAIMAO', '玳瑁猫'),
        ('OTHER', '其他'),
        null=True,
        )

    BirthMonth = create_choices_class(
        'BirthMonth',
        ('SPRING', '春天'),
        ('SUMMER', '夏天'),
        ('AUTUMN', '秋天'),
        ('WINTER', '冬天'),
        ('FIRST_HALF', '上半年'),
        ('LATTER_HALF', '下半年'),
        *[(f'MONTH{i}', f'{i}月') for i in range(1,13)],
        null=True,
    )

    BirthDay = create_choices_class(
        'BirthDay',
        ('EARLY', '上旬'),
        ('MIDDLE', '中旬'),
        ('LATE', '下旬'),
        *[(f'DAY{i}', f'{i}日') for i in range(1, 32)],
        null=True,
    )

    Status = create_choices_class(
        'Status',
        ('HOMELESS', '在校流浪'),
        ('MISSING', '失踪'),
        ('PASSAWAY', '回喵星'),
        ('ADOPTED', '已领养'),
        ('HOSPITAL', '住院'),
        null=True,
        null_label = '状态不明',
        )

    # Static infomation
    name = models.CharField('名字', max_length=16, blank=True)
    old_name = models.CharField('曾用名', max_length=32, blank=True)
    gender = models.BooleanField('性别', null=True, blank=True, choices=Gender.choices)
    fur = models.BooleanField('发量', null=True, blank=True, choices=Fur.choices)
    cat_type = models.PositiveSmallIntegerField('毛色', choices=CatType.choices)

    birth_year = models.PositiveSmallIntegerField('出生年', null=True, blank=True)
    birth_month = models.PositiveSmallIntegerField('出生月', null=True, blank=True, choices=BirthMonth.choices)
    birth_day = models.PositiveSmallIntegerField('出生日', null=True, blank=True, choices=BirthDay.choices)

    campus = models.ForeignKey(
        'campus.Campus', 
        verbose_name='校区', 
        related_name='cats',
        related_query_name='cat',
        on_delete=models.CASCADE,
        )
    mom = models.ForeignKey(
        'self', 
        verbose_name='猫妈',
        related_name='kids',
        related_query_name='kid', 
        on_delete=models.SET_NULL,
        limit_choices_to={'gender': Gender.GIRL.value},
        null=True,
        blank=True,
        )

    # status
    neutered = models.BooleanField('已绝育', null=True, blank=True, 
                                   choices=[(True, '已绝育'), (False, '未绝育'), (None, '未知')])
                                   # Make rendering the same as other fields: get_neutered_display()
    status = models.PositiveSmallIntegerField('状态', null=True, blank=True, choices=Status.choices)

    class Meta:
        verbose_name = '猫猫'
        verbose_name_plural = '猫猫'
        constraints = [
            models.UniqueConstraint(fields=['name', 'campus'], name='unique_name')
        ]   # Cats in the same campus can not have same name.
        ordering = ['pk']    # Paginator needs an ordering.
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class CatDetail(models.Model):
    """猫猫的数据库附表，用于存储不经常查找的 column"""
    
    Source = create_choices_class(
        'Source',
        ('REPRODUCE', '流浪二代'),
        ('ABANDON', '弃养'),
        ('MIGRATE', '校外流浪猫'),
        null=True,
        )

    cat = models.OneToOneField(
        Cat,
        verbose_name='主模型', 
        related_name='detail',
        on_delete=models.CASCADE
        )
    description = models.TextField('描述', blank=True)
    source = models.PositiveSmallIntegerField('来源', null=True, blank=True, choices=Source.choices)
    last_update = models.DateField('最近更新')
    documented_date = models.DateField('档案创建', auto_now_add=True)
    parent = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        verbose_name='紧急联系人', 
        on_delete=models.SET_NULL,
        related_name='kids',
        related_query_name='kid',
        null=True,
        blank=True
        )
    avatar = models.ForeignKey(
        'file.Photo', 
        verbose_name='头像',
        related_name='+',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
        )
    cover_photo = models.ForeignKey(
        'file.Photo', 
        verbose_name='封面照',
        related_name='+',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
        )

    class Meta:
        verbose_name = '详细信息'
        verbose_name_plural = '详细信息'

    def __str__(self):
        return f'{self.cat!s}-详细信息'


class Entry(models.Model):
    """猫咪状态变更记录的数据库模型"""
    name = models.CharField('名称', max_length=4)
    description = models.CharField('详细信息', max_length=128, blank=True)
    date = models.DateField('日期')
    cat = models.ForeignKey(
        Cat, 
        verbose_name='猫猫', 
        related_name='entries',
        related_query_name='entry',
        on_delete=models.CASCADE,
        )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        verbose_name='记录者', 
        on_delete=models.SET_NULL,
        null=True,
        # blank=False here, null is only reserved for SET_NULL
        )

    class Meta:
        verbose_name = '记录'
        verbose_name_plural = '记录'
        indexes = [
            models.Index(fields=['cat']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f'{self.cat!s}-{self.name}-{self.date!s}'