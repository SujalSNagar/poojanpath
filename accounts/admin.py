from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    model = User

    ordering = ('mobile_number',)

    list_display = (
        'mobile_number',
        'email',
        'is_staff',
        'is_superuser',
    )

    fieldsets = (
        (None, {
            'fields': (
                'mobile_number',
                'password',
            )
        }),

        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'mobile_number',
                'email',
                'password1',
                'password2',
                'is_staff',
                'is_superuser',
            ),
        }),
    )

    search_fields = (
        'mobile_number',
        'email',
    )