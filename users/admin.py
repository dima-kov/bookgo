from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import User


class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional info', {'fields': ('about', 'avatar', )}),
        ('Preferences', {'fields': (
            'favourite_book', 'favourite_author',
            'reading_preferences')}),
        ('Delivery preferences', {'fields': ('city', 'novaposhta_number', )}),
    )


admin.site.register(User, UserAdmin)
