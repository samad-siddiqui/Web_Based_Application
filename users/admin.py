from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        'email', 'first_name', 'last_name', 'is_active', 'is_superuser')
    ordering = ('email',)
    search_fields = ('email', 'first_name', 'last_name')

    fieldsets = (
        ('Basic Info', {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': (
          'email', 'first_name', 'last_name', 'password1', 'password2',
         'is_staff', 'is_superuser'
         ),
        }),
    )


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ('user', 'user__first_name', 'user__last_name', 'status')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
