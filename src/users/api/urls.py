from django.urls import path
from rest_framework.authtoken import views as auth_views
from . import views

urlpatterns = [
    path('token-auth/', auth_views.obtain_auth_token, 'get_token'),
    path('reset-passwd/', views.ChangePasswordView.as_view(), 'reset_passwd')
]
