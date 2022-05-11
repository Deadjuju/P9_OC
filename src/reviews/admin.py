from django.contrib import admin

from reviews.models import Ticket, Review


class TicketAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "user", )
    fields = ("title", "user", "description", "image", )
    search_fields = ['title', ]
    search_help_text = "Titre du ticket"


admin.site.register(Ticket, TicketAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("ticket", "user", "headline", )
    fields = ("ticket", "user", "headline", "body", )


admin.site.register(Review, ReviewAdmin)
