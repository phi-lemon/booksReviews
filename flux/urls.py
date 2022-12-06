from django.urls import path

from . import views

urlpatterns = [
    path('', views.feed, name='index'),
    path('ticket/<int:pk>/', views.edit_ticket, name='edit_ticket'),
    path('ticket/new/', views.edit_ticket, name='create_ticket'),
    # path('review/<int:pk>/', views.edit_review, name='edit_review'),
    path('review/<int:pk>/', views.create_review_from_ticket, name='create_review_from_ticket'),
    path('review/new/', views.create_review, name='create_review'),
]
