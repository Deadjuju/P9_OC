from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect

from authentication import forms


def signup(request):
    form = forms.SignupForm()
    if request.method == "POST":
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            success_message = f"Bonjour <strong>{user.username}</strong>,<br>" \
                              f"Bienvenue chez LITReview!"
            messages.add_message(request, messages.SUCCESS, message=success_message)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request,
                  'authentication/signup.html',
                  context={'form': form})
