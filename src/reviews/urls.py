from django.urls import path

from reviews import views

urlpatterns = [
    path('', views.home, name="home"),
    path('posts', views.user_posts, name="posts"),
    path('create-ticket/', views.CreateTicketView.as_view(), name="create_ticket"),
    path('ticket/<int:ticket_id>/edit/', views.edit_ticket, name="edit_ticket"),
    path('ticket/<int:ticket_id>/delete/', views.delete_ticket, name="delete_ticket"),
    path('create-review/', views.create_review, name="create_review"),
    path('review/<int:review_id>/edit/', views.edit_review, name="edit_review"),
    path('review/<int:review_id>/delete/', views.delete_review, name="delete_review"),
    path('subscribers/', views.subscribers_subscriptions, name="subscribers"),
    path('unsubscribe/<int:subscribers_id>/delete/', views.unsubscribe, name='unsubscribe'),
    path('reply/<int:ticket_id>/', views.reply_to_a_ticket, name='reply'),
]
