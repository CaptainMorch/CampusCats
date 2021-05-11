from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.
contact_fieldset = ('Contact Info', {'fields': ('phone', 'qq', 'wx_id')})

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (contact_fieldset,)
    add_fieldsets = UserAdmin.add_fieldsets + (contact_fieldset,)