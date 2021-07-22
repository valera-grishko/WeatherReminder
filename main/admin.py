from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Follow
from .forms import CustomUserCreationForm


class CustomUserAdmin(UserAdmin):
    model = User
    add_form = CustomUserCreationForm

    fieldsets = (
        *UserAdmin.fieldsets, (
            'User role',
            {
                'fields': (
                    'notifications',
                    'period'
                )
            }
        )
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Follow)
