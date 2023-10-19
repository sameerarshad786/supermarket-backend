from django.contrib import admin

from users.models import User, Profile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id", "email", "is_online", "is_staff", "is_superuser"
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id", "user", "full_name", "gender", "image"
    )
