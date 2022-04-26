from django.urls import path

from reviews import views

urlpatterns = [
    path('', views.home, name="home"),
]
