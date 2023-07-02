from django.contrib import admin

from users_api.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ['profile_id', 'email', 'username', 'name', 'is_superuser', 'is_staff']
