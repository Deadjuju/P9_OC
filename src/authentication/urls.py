from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

import authentication.views

urlpatterns = [
    path('', LoginView.as_view(
        template_name="authentication/login.html",
        redirect_authenticated_user=True,
    ), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('signup/', authentication.views.signup, name="signup"),
    path(
        'change-password/',
        authentication.views.PasswordChangeView.as_view(),
        name="password_change"),
]
