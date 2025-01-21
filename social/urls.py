from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from .views import ObtainUserFromToken, SettingsUpdateView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),   
    
    path('user/', ObtainUserFromToken.as_view(), name='obtain_user_from_token'),
    path('user/settings/update/', SettingsUpdateView.as_view(), name='user_settings_update'),
]