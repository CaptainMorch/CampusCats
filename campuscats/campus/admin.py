from django.contrib import admin
from .models import Campus, Location

# Register your models here.
admin.site.register((Campus, Location,))