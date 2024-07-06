from django.urls import path
from apps.accounts import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register-v1/', views.RegisterAPIView.as_view(), name='register-v1'),
    path('register-v2/', views.UserUpdateApiView.as_view(), name='register-v2'),
    path('activate-account/', views.ActivateUserApiView.as_view(), name='activate-account'),
]
