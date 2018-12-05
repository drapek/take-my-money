from django.urls import path
from rest_framework.authtoken import views as auth_views
from . import views

urlpatterns = [
    path('token-auth/', auth_views.obtain_auth_token, name='get-token'),
    path('reset-passwd/', views.ChangePasswordView.as_view(), name='reset-passwd'),
    path('<int:pk>/', views.UserDetails.as_view(), name='user-details'),
]
