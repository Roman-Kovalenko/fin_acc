from django.utils.translation import gettext_lazy as _
from django.urls import path
from django.contrib.auth import views

from .views import SignUpView, ProfileView


urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(
        template_name='users/login.html',
        extra_context={'title': _('Main page')}
    ), name='login'),
    path('logout/', views.LogoutView.as_view(
        template_name='users/logged_out.html'), name='logout'),

    path('password_change/', views.PasswordChangeView.as_view(
        template_name='users/password_change_form.html',
        extra_context={'title': _('Password Change')}
    ), name='password_change'),
    path('password_change/done/', views.PasswordChangeDoneView.as_view(
        template_name='users/password_change_done.html',
        extra_context={'title': _('Password Change')}
    ), name='password_change_done'),

    path('password_reset/', views.PasswordResetView.as_view(
        template_name='users/password_reset_form.html'
    ), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'
    ), name='password_reset_complete'),
]
