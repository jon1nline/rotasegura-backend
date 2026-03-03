from django.contrib import admin
from .models import UserProfile, History


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'phone', 'level', 'xp', 'max_xp']
	search_fields = ['user__username', 'user__email']


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'title', 'status', 'likes', 'views', 'verified', 'created_at']
	list_filter = ['status', 'verified', 'created_at']
	search_fields = ['title', 'location', 'user__username']
