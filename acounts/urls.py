from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name = 'register'),
    path('logout/', views.logout, name = 'logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgot_password/', views.forgotPassword, name = 'forgotPassword'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
]
