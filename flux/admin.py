from django.contrib import admin
from . import models


admin.site.register(models.Review)


class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'user')


admin.site.register(models.Ticket, TicketAdmin)

