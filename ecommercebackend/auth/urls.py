from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterUserAPIView.as_view(), name='register'),
    path('login/', views.LoginUserAPIView.as_view(), name='login'),
    path('logout/', views.UserLogoutAPIView.as_view(), name='logout'),
    # other paths
]
