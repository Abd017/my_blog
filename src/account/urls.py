from django.urls import path
from .views import login, register, logout_view
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('login/', LoginView.as_view(template_name='account/login.html'), name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
]