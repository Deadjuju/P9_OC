from django.urls import path

from reviews import views

urlpatterns = [
    path('', views.home, name="home"),
    path('create-ticket/', views.CreateTicketView.as_view(), name="create_ticket"),
    path('create-review/', views.create_review, name="create_review"),
]
