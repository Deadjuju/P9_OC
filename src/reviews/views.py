from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from authentication.models import User
from . import forms, models


@login_required
def home(request):

    # tickets = models.Ticket.objects.filter(user__in__followed_by=request.user)

    followed_users = models.UserFollows.objects.filter(user=request.user)
    subscriptions = [user.followed_user for user in followed_users]
    print(f"Users: {subscriptions}")

    # display feed according to subscriptions
    users_filter = Q(user__in=subscriptions) | Q(user=request.user)
    tickets = models.Ticket.objects.filter(users_filter)
    reviews = models.Review.objects.filter(users_filter)

    # tickets = models.Ticket.objects.all()
    # reviews = models.Review.objects.all()

    return render(request,
                  'reviews/home.html',
                  context={"tickets": tickets,
                           "reviews": reviews})


# @login_required
# def create_ticket(request):
#     ticket_form = forms.TicketForm()
#
#     if request.method == "POST":
#         ticket_form = forms.TicketForm(request.POST, request.FILES)
#         if ticket_form.is_valid():
#             ticket = ticket_form.save(commit=False)
#             ticket.user = request.user
#             ticket.save()
#         return redirect('home')
#
#     return render(request,
#                   'reviews/create-ticket.html',
#                   context={'ticket_form': ticket_form})


class CreateTicketView(LoginRequiredMixin, CreateView):
    model = models.Ticket
    template_name = 'reviews/create-ticket.html'
    form_class = forms.TicketForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# class CreateReviewView(LoginRequiredMixin, CreateView):
#     model = models.Review
#     template_name = 'review/create-review.html'
#     form_class = [models.Ticket, models.Review]
#     success_url = reverse_lazy('home')
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)
#


@login_required
def create_review(request):
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()

    if request.method == "POST":
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
        return redirect('home')

    return render(request,
                  'reviews/create-review.html',
                  context={'ticket_form': ticket_form,
                           'review_form': review_form})


@login_required
def subscribers_subscriptions(request):
    form = forms.SubscriberForm()
    context = {'form': form}

    # display subscriptions
    subscriptions = models.UserFollows.objects.filter(user=request.user)
    context['subscriptions'] = subscriptions

    # display subscribers
    subscribers = models.UserFollows.objects.filter(followed_user=request.user)
    context['subscribers'] = subscribers

    if request.method == "POST":

        # followed_user = get_object_or_404(User, username=request.POST['followed_user'])

        # get the searched user
        try:
            new_followed_user = get_object_or_404(User, username=request.POST['followed_user'])
        except ObjectDoesNotExist:
            error_message = f"--- {request.POST['followed_user'].upper()} --- n'existe pas dans la bdd."
            messages.add_message(request, messages.ERROR, message=error_message)
            return render(request,
                          "reviews/subs.html",
                          context=context)
        else:
            # case where one is looking for oneself
            if new_followed_user.username == request.user.username:
                error_message = " --- Vous ne pouvez pas vous suivre vous même! --- "
                messages.add_message(request, messages.ERROR, message=error_message)
                return render(request,
                              "reviews/subs.html",
                              context=context)

            # subscription registration
            new_subscription = models.UserFollows(user=request.user, followed_user=new_followed_user)
            try:
                new_subscription.save()
            except IntegrityError:
                error_message = f"Vous suivez déjà {new_followed_user}."
                messages.add_message(request, messages.ERROR, message=error_message)
                return render(request,
                              "reviews/subs.html",
                              context=context)
            else:
                success_message = f"Vous suivez désormais {new_subscription.followed_user}"
                messages.add_message(request, messages.SUCCESS, message=success_message)
                return render(request,
                              "reviews/subs.html",
                              context=context)

    return render(request,
                  "reviews/subs.html",
                  context=context)


@login_required
def unsubscribe(request, subscribers_id):
    if request.method == "POST":
        user_to_unsubscribe = get_object_or_404(models.UserFollows, id=subscribers_id)
        user_to_unsubscribe.delete()

        success_message = f"Vous ne suivez plus {user_to_unsubscribe.followed_user}."
        messages.add_message(request, messages.SUCCESS, message=success_message)
        return redirect('subscribers')
