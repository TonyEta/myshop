from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_view, login_view, logout_view



app_name = 'users'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='users/forgot_password.html',
        email_template_name='users/password_reset_email.html',
        success_url='/users/password_reset/done/'
    ), name='password-reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'
    ), name='password-reset-done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html',
             success_url='/users/password_reset_complete/'
         ), 
         name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'
    ), name='password-reset-complete')
    
]