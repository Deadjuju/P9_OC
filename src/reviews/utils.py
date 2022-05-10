from typing import List

from django.db.models import Q
from django.db.models.query import QuerySet

from authentication.models import User
from reviews import models


def get_users_subscriptions(user: User) -> List:
    """ retrieves the list of user subscriptions """

    followed_users = models.UserFollows.objects.filter(user=user)
    subscriptions = [f_user.followed_user for f_user in followed_users]
    return subscriptions


def get_users_viewable_reviews(user: User) -> QuerySet:
    """ tickets to display in the feed """

    subscriptions = get_users_subscriptions(user=user)
    reviews = models.Review.objects.filter(
        Q(user__in=subscriptions) | Q(user=user) | Q(ticket__user=user)
    )
    return reviews


def get_users_viewable_tickets(user: User) -> QuerySet:
    """ reviews to display in the feed """

    subscriptions = get_users_subscriptions(user=user)
    tickets = models.Ticket.objects.filter(
        Q(user__in=subscriptions) | Q(user=user)
    )
    return tickets
