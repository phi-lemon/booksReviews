from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('', include('django.contrib.auth.urls')),
    path('users/', views.user_list, name='user_list'),
    path('users/follow/', views.user_follow, name='user_follow'),  # BEFORE path('users/<username>/'... !!!
    path('users/<username>/', views.user_detail, name='user_detail'),

]