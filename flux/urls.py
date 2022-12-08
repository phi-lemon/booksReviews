from django.urls import path

from . import views

urlpatterns = [
    path('', views.feed, name='index'),
    path('ticket/<int:pk>/', views.edit_ticket, name='edit_ticket'),
    path('ticket/new/', views.create_ticket, name='create_ticket'),
    path('review/<int:pk>/', views.create_review_from_ticket, name='create_review_from_ticket'),
    path('review/new/', views.create_review, name='create_review'),
    path('review/edit/<int:pk>/', views.edit_review, name='edit_review'),
    path('posts/posts/', views.user_posts, name='posts'),
    path('posts/ticket/delete/<int:pk>', views.TicketDeleteView.as_view(), name='delete_ticket'),
    path('posts/review/delete/<int:pk>', views.ReviewDeleteView.as_view(), name='delete_review'),
]
