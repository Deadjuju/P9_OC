from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

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


class PasswordChangeView(FormView):
    template_name = 'authentication/password_change_form.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('posts')

    def get_form_kwargs(self):
        kwargs = super(PasswordChangeView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        success_message = "Votre mot de passe a bien été changé."
        messages.add_message(self.request, messages.SUCCESS, message=success_message)
        return super(FormView, self).form_valid(form)
