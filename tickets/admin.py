from django.contrib import admin

from .models import Ticket, TicketUpdate


class TicketUpdateInline(admin.TabularInline):
    model = TicketUpdate
    extra = 0


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "requester_name", "category", "priority", "status", "created_at")
    list_filter = ("status", "priority", "category", "created_at")
    search_fields = ("title", "requester_name", "requester_email", "description")
    inlines = [TicketUpdateInline]


@admin.register(TicketUpdate)
class TicketUpdateAdmin(admin.ModelAdmin):
    list_display = ("ticket", "author", "created_at")
    search_fields = ("note", "author", "ticket__title")

# Register your models here.
