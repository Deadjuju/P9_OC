from django.contrib import admin

from reviews.models import Ticket, Review


class TicketAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "user", )
    fields = ("title", "user", "description", "image", )
    search_fields = ['title', ]
    search_help_text = "Titre du ticket"
    list_filter = ("user", )
    autocomplete_fields = ("user", )


admin.site.register(Ticket, TicketAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("ticket", "user", "headline", )
    fields = ("ticket", "user", "headline", "body", )
    list_filter = ("user", )
    autocomplete_fields = ("user", )


admin.site.register(Review, ReviewAdmin)
