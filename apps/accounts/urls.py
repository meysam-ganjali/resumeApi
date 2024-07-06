from django.urls import path
from apps.accounts import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register-v1/', views.RegisterAPIView.as_view(), name='register-v1'),
    path('register-v2/', views.UserUpdateApiView.as_view(), name='register-v2'),
    path('activate-account/', views.ActivateUserApiView.as_view(), name='activate-account'),
    path('education/', views.AddUserEducationView.as_view(), name='user-education-create'),
    path('education/<int:pk>/', views.UpdateUserEducationView.as_view(), name='user-education-update'),
    path('workexperience/', views.AddUserWorkExperience.as_view(), name='user-work-experience-create'),
    path('workexperience/<int:pk>/', views.UpdateUserWorkExperience.as_view(), name='user-work-experience-update'),
    path('skill/', views.AddUserSkillApiView.as_view(), name='user-skill-create'),
    path('skill/<int:pk>/', views.UpdateUserSkillApiView.as_view(), name='user-skill-update'),
    path('work-samples/', views.AddUserWorkSamples.as_view(), name='user-work-samples-create'),
    path('work-samples/<int:pk>/', views.UpdateUserWorkSamples.as_view(), name='user-work-samples-update'),
]
