from django.urls import path
from rest_framework.authtoken import views as auth_views
from . import views

urlpatterns = [
    path('token-auth/', auth_views.obtain_auth_token, name='get-token'),
    path('reset-passwd/', views.ChangePasswordView.as_view(), name='reset-passwd'),
    path('<int:pk>/', views.UserDetails.as_view(), name='user-details'),
    path('invite/', views.UserInvitation.as_view(), name='user-invitation'),
    path('registration/<uuid:hash>/', views.UserRegistration.as_view(), name='user-registration'),
    path('/', views.UserListSearchView.as_view(), name='user-search'),
    path('search/<str:search_pattern>/', views.UserListSearchView.as_view(), name='user-search-filtered'),
]
