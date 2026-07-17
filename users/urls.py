from django.urls import path
from .views import register_view, login_view, logout_view, renew_password_view


app_name = 'users'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('renew/', renew_password_view, name='renew-password'),
]