from django.contrib import admin

from .models import (
    Asset,
    AuditLog,
    Department,
    KnowledgeArticle,
    Notification,
    Ticket,
    TicketAttachment,
    TicketUpdate,
    UserProfile,
)


class TicketUpdateInline(admin.TabularInline):
    model = TicketUpdate
    extra = 0


class TicketAttachmentInline(admin.TabularInline):
    model = TicketAttachment
    extra = 0


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("ticket_number", "title", "requester_name", "assigned_to", "category", "priority", "status", "created_at")
    list_filter = ("status", "priority", "category", "assigned_to", "created_at")
    search_fields = ("title", "requester_name", "requester_email", "description")
    inlines = [TicketUpdateInline, TicketAttachmentInline]


@admin.register(TicketUpdate)
class TicketUpdateAdmin(admin.ModelAdmin):
    list_display = ("ticket", "author", "created_at")
    search_fields = ("note", "author", "ticket__title")


admin.site.register(Department)
admin.site.register(UserProfile)
admin.site.register(TicketAttachment)
admin.site.register(KnowledgeArticle)
admin.site.register(Asset)
admin.site.register(Notification)
admin.site.register(AuditLog)

# Register your models here.
