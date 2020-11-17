from django.db import models

# Create your models here.
class Campus(models.Model):
    """校区数据库模型"""
    name = models.CharField('简称', max_length=4)
    full_name = models.CharField('全称', max_length=16)

    # Fields for amap support
    longitude = models.FloatField('经度')
    latitude = models.FloatField('纬度')
    zoom = models.PositiveSmallIntegerField('缩放级别')

    class Meta:
        verbose_name = '校区'
        verbose_name_plural = '校区'

    def __str__(self):
        return self.name


class Location(models.Model):
    """校内猫咪活动位置数据库模型"""
    name = models.CharField('名称', max_length=16)
    campus = models.ForeignKey(
        Campus,
        verbose_name='校区',
        related_name='locations',
        related_query_name='location',
        on_delete=models.CASCADE
        )
    longitude = models.FloatField('经度')
    latitude = models.FloatField('纬度')

    class Meta:
        verbose_name = '位置'
        verbose_name_plural = '位置'

    def __str__(self):
        return str(self.campus) + self.name
