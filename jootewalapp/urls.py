from django.urls import path, include
from . import views

urlpatterns = [
    path('register', views.user_register_f),
]