from django.conf import settings
from django.db import models


class Ticket(models.Model):
    title = models.CharField(max_length=128, verbose_name="Titre")
    description = models.TextField(max_length=2048, blank=True, verbose_name="Description")
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Utilisateur")
    image = models.ImageField(null=True, blank=True, verbose_name="Image")
    time_created = models.DateTimeField(auto_now_add=True)
