from django.contrib import admin
from .models import Cat, CatDetail, Entry

# Register your models here.
admin.site.register((Cat, CatDetail, Entry))