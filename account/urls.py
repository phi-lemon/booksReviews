from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('', include('django.contrib.auth.urls')),
]