from django.contrib import admin
from . import models


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('headline', 'ticket', 'user')


admin.site.register(models.Review, ReviewAdmin)


class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'user')


admin.site.register(models.Ticket, TicketAdmin)

