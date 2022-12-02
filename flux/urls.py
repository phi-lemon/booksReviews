from django.urls import path

from . import views

urlpatterns = [
    path('', views.feed, name='index'),
    path('ticket/<int:pk>/', views.edit_ticket, name='edit_ticket'),
    path('ticket/new/', views.edit_ticket, name='create_ticket')
]
