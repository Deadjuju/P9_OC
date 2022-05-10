from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from authentication.models import User
from . import forms, models
from .utils import get_users_viewable_tickets, get_users_viewable_reviews


@login_required
def home(request):
    """ feed display on main page """

    tickets = get_users_viewable_tickets(user=request.user)
    reviews = get_users_viewable_reviews(user=request.user)

    #  chain the 2 parameters
    tickets_and_reviews = sorted(
        chain(tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True
    )

    paginator = Paginator(tickets_and_reviews, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj,
               "home_page": True}

    return render(request,
                  'reviews/home.html',
                  context=context)


@login_required
def user_posts(request):

    tickets = models.Ticket.objects.filter(user=request.user)
    reviews = models.Review.objects.filter(user=request.user)

    #  chain the 2 parameters
    tickets_and_reviews = sorted(
        chain(tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True
    )

    context = {"tickets_and_reviews": tickets_and_reviews, }
    return render(request,
                  'reviews/posts.html',
                  context=context)


class CreateTicketView(LoginRequiredMixin, CreateView):
    model = models.Ticket
    template_name = 'reviews/create-ticket.html'
    form_class = forms.TicketForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@login_required
def edit_ticket(request, ticket_id: int):
    ticket = get_object_or_404(models.Ticket, pk=ticket_id)
    if request.user == ticket.user:
        ticket_form = forms.TicketForm(instance=ticket)
        if request.method == "POST":
            ticket_form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
            if ticket_form.is_valid():
                ticket.save()
                success_message = f"Le billet <strong>{ticket.title}</strong>> a bien été mis à jour."
                messages.add_message(request, messages.SUCCESS, message=success_message)
                return redirect("posts")

        context = {'ticket_form': ticket_form,
                   'ticket': ticket}
        return render(request,
                      "reviews/edit-ticket.html",
                      context=context)
    else:
        return redirect("posts")


@login_required
def delete_ticket(request, ticket_id: int):
    if request.method == "POST":
        ticket_to_delete = get_object_or_404(models.Ticket, id=ticket_id)
        ticket_to_delete.delete()
        success_message = f"Le billet <strong>{ticket_to_delete.title}</strong> a bien été supprimé."
        messages.add_message(request, messages.SUCCESS, message=success_message)
        return redirect('posts')


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
def edit_review(request, review_id: int):
    review = get_object_or_404(models.Review, pk=review_id)
    ticket = review.ticket
    review_form = forms.ReviewForm(instance=review)
    if request.method == "POST":
        review_form = forms.ReviewForm(request.POST, instance=review)
        if review_form.is_valid():
            review.save()
            success_message = f"La critique de <strong>{ticket.title}</strong> a bien été mis à jour."
            messages.add_message(request, messages.SUCCESS, message=success_message)
            return redirect("posts")

    context = {'review_form': review_form,
               'ticket': ticket}
    return render(request,
                  "reviews/edit-review.html",
                  context=context)


@login_required
def delete_review(request, review_id):
    review_to_delete = get_object_or_404(models.Review, id=review_id)
    ticket = get_object_or_404(models.Ticket, pk=review_to_delete.ticket.pk)
    review_to_delete.delete()
    ticket.already_replied = False
    ticket.save(update_fields=['already_replied'])
    success_message = f"La critique de <strong>{review_to_delete.ticket.title}</strong> a bien été supprimé."
    messages.add_message(request, messages.SUCCESS, message=success_message)
    return redirect('posts')


@login_required
def reply_to_a_ticket(request, ticket_id: int):
    ticket = get_object_or_404(models.Ticket, pk=ticket_id)
    if not ticket.already_replied:
        review_form = forms.ReviewForm()

        if request.method == "POST":
            review_form = forms.ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = request.user
                review.ticket = ticket
                review.save()
                ticket.already_replied = True
                ticket.save(update_fields=['already_replied'])
            return redirect('home')

        context = {"review_form": review_form,
                   "ticket": ticket, }
        return render(request,
                      'reviews/reply.html',
                      context=context)
    return redirect("home")


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

        # get the searched user
        try:
            new_followed_user = User.objects.get(username=request.POST['followed_user'])
        except ObjectDoesNotExist:
            error_message = f"<strong>{request.POST['followed_user'].upper()}" \
                            f"</strong> n'existe pas dans la base de donnée."
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
                error_message = f"Vous suivez déjà <strong>{new_followed_user}</strong>."
                messages.add_message(request, messages.ERROR, message=error_message)
                return render(request,
                              "reviews/subs.html",
                              context=context)
            else:
                success_message = f"Vous suivez désormais <strong>{new_subscription.followed_user}</strong>."
                messages.add_message(request, messages.SUCCESS, message=success_message)
                return render(request,
                              "reviews/subs.html",
                              context=context)

    return render(request,
                  "reviews/subs.html",
                  context=context)


@login_required
def unsubscribe(request, subscribers_id: int):
    if request.method == "POST":
        user_to_unsubscribe = get_object_or_404(models.UserFollows, id=subscribers_id)
        user_to_unsubscribe.delete()

        success_message = f"Vous ne suivez plus <strong>{user_to_unsubscribe.followed_user}</strong>."
        messages.add_message(request, messages.SUCCESS, message=success_message)
        return redirect('subscribers')
