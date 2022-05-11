from django.contrib import admin

from authentication.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name", )
    fields = ("username", "email", ("first_name", "last_name",), "date_joined", )
    search_fields = ['username', ]
    search_help_text = "Pseudo de l'utilisateur"


admin.site.register(User, UserAdmin)
