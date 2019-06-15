from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

app_name = 'main'
urlpatterns = [
    path('', views.home, name='home'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('form', views.form, name='form'),
    path('additions', views.additions, name='additions'),
    path('password-reset/', PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('accounts/login/', views.signin, name='accounts_signin')
]
