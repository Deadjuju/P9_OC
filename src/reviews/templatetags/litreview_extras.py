from django import template
from django.utils import timezone


MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR
DAYS = 2 * DAY


register = template.Library()


@register.filter
def model_type(instance):
    return type(instance).__name__


@register.filter
def get_posted_at_display(posted_at):
    seconds_ago = (timezone.now() - posted_at).total_seconds()
    if seconds_ago <= HOUR:
        return f"Publié il y a {int(seconds_ago // MINUTE)} minutes."
    elif seconds_ago <= DAY:
        return f"Publié il y a {int(seconds_ago // HOUR)} heures."
    elif seconds_ago <= DAYS:
        return f"Publié hier, à {posted_at.strftime('%Hh%M')}."
    return f"Publié le {posted_at.strftime('%d %b %y à %Hh%M')}"


@register.simple_tag(takes_context=True)
def get_poster_display(context, user):
    if user == context['user']:
        return 'Vous avez '
    return f"{user.username} a "


@register.simple_tag()
def rating_star_display(rating):
    return f"{rating * '★'} { (5 - rating) * '☆'}"
