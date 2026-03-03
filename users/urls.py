from django.urls import path
from .views import register_view, login_view, user_profile_view, user_profile_update_view, user_history_view

urlpatterns = [
    path('auth/register/', register_view, name='auth-register'),
    path('auth/login/', login_view, name='auth-login'),
    path('user/profile/', user_profile_view, name='user-profile'),
    path('user/profile/update/', user_profile_update_view, name='user-profile-update'),
    path('user/history/', user_history_view, name='user-history'),
]
