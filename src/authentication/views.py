from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView

from authentication import forms, models


class SignupView(CreateView):
    """ Manage new user registration """

    model = models.User
    template_name = 'authentication/signup.html'
    form_class = forms.SignupForm
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)

    def form_valid(self, form):
        super(SignupView, self).form_valid(form)
        user = form.save()
        login(self.request, user)
        success_message = f"Bonjour <strong>{self.request.user.username}</strong>,<br>" \
                          f"Bienvenue chez LITReview!"
        messages.add_message(self.request, messages.SUCCESS, message=success_message)
        return redirect(settings.LOGIN_REDIRECT_URL)


class PasswordChangeView(FormView):
    """ Change user password """

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
