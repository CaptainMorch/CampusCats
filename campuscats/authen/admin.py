from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import User, Contact


class ContactInline(admin.TabularInline):
    model = Contact

class UserAdmin(DefaultUserAdmin):
    inlines = [
        ContactInline,
    ]

admin.site.register(User, UserAdmin)