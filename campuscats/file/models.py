from datetime import date
from django.db import models
from django.conf import settings

# Create your models here.
class Photo(models.Model):
    """猫咪相片的数据库模型"""
    image = models.ImageField('图像', upload_to='image/')
    title = models.CharField('标题', blank=True, max_length=8)
    description = models.TextField('描述', blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='拍摄者',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='photos',
        related_query_name='photo'
    )    # choose one between 'author' relationship or 'autor_name' string
    author_name = models.CharField('拍摄者名称', max_length=16, blank=True)
    date = models.DateField('拍摄日期', default=date.today, null=True, blank=True)
    cats = models.ManyToManyField(
        'cat.Cat',
        verbose_name='出镜猫猫们',
        related_name='photos',
        related_query_name='photo'
    )

    class Meta:
        verbose_name = '相片'
        verbose_name_plural = '相片'

    def __str__(self):
        return self.title