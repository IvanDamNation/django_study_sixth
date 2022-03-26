from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterView, upgrade_me, UserUpdateView

urlpatterns = [
    path('',
         LoginView.as_view(template_name='accounts_login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(template_name='accounts_logout.html'),
         name='logout'),
    path('register/',
         BaseRegisterView.as_view(template_name='accounts_register.html'),
         name='signup'),
    path('upgrade/',
         upgrade_me,
         name='upgrade'),
    path('edit/', UserUpdateView.as_view(), name='user_update'),

]
