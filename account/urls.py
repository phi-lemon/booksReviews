from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('', include('django.contrib.auth.urls')),
    path('users/follow/', views.user_follow, name='user_follow'),  # form action url - BEFORE path('users/<username>/' !
    path('users/abonnements/', views.user_detail, name='user_detail'),
]