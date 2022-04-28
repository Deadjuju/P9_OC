from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from . import forms, models


@login_required
def home(request):

    tickets = models.Ticket.objects.all()
    reviews = models.Review.objects.all()

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
