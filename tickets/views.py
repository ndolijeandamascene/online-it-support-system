from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from .forms import TicketAttachmentForm, TicketForm, TicketStatusForm, TicketUpdateForm
from .models import AuditLog, KnowledgeArticle, Notification, Ticket


def ticket_list(request):
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()
    tickets = Ticket.objects.all()

    if query:
        tickets = tickets.filter(
            Q(title__icontains=query)
            | Q(requester_name__icontains=query)
            | Q(requester_email__icontains=query)
            | Q(description__icontains=query)
        )

    if status:
        tickets = tickets.filter(status=status)

    stats = Ticket.objects.values("status").annotate(total=Count("id"))

    return render(
        request,
        "tickets/ticket_list.html",
        {
            "tickets": tickets,
            "query": query,
            "status": status,
            "statuses": Ticket.Status.choices,
            "stats": {item["status"]: item["total"] for item in stats},
        },
    )


def dashboard(request):
    stats = Ticket.objects.values("status").annotate(total=Count("id"))
    priority_stats = Ticket.objects.values("priority").annotate(total=Count("id"))
    recent_tickets = Ticket.objects.select_related("assigned_to", "department")[:6]

    return render(
        request,
        "tickets/dashboard.html",
        {
            "stats": {item["status"]: item["total"] for item in stats},
            "priority_stats": {item["priority"]: item["total"] for item in priority_stats},
            "statuses": Ticket.Status.choices,
            "priorities": Ticket.Priority.choices,
            "recent_tickets": recent_tickets,
        },
    )


@require_http_methods(["GET", "POST"])
def ticket_create(request):
    form = TicketForm(request.POST or None)
    attachment_form = TicketAttachmentForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        ticket = form.save()
        if request.FILES and attachment_form.is_valid():
            attachment = attachment_form.save(commit=False)
            attachment.ticket = ticket
            attachment.uploaded_by = attachment.uploaded_by or ticket.requester_name
            attachment.save()
        AuditLog.objects.create(action="Ticket created", ticket=ticket, details=ticket.title)
        messages.success(request, "Support ticket created successfully.")
        return redirect(ticket)

    return render(request, "tickets/ticket_form.html", {"form": form, "attachment_form": attachment_form})


@require_http_methods(["GET", "POST"])
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    status_form = TicketStatusForm(request.POST or None, instance=ticket, prefix="status")
    update_form = TicketUpdateForm(request.POST or None, prefix="update")
    attachment_form = TicketAttachmentForm(request.POST or None, request.FILES or None, prefix="attachment")

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "status" and status_form.is_valid():
            ticket = status_form.save(commit=False)
            if ticket.status == Ticket.Status.RESOLVED and ticket.resolved_at is None:
                ticket.resolved_at = timezone.now()
            if ticket.status == Ticket.Status.CLOSED and ticket.closed_at is None:
                ticket.closed_at = timezone.now()
            ticket.save()
            Notification.objects.create(ticket=ticket, recipient=ticket.assigned_to, message=f"{ticket.ticket_number} was updated.")
            AuditLog.objects.create(action="Ticket status updated", ticket=ticket, details=ticket.status)
            messages.success(request, "Ticket status updated.")
            return redirect(ticket)
        if action == "note" and update_form.is_valid():
            note = update_form.save(commit=False)
            note.ticket = ticket
            note.save()
            AuditLog.objects.create(action="Ticket note added", ticket=ticket, details=note.note[:200])
            messages.success(request, "Update added to the ticket.")
            return redirect(ticket)
        if action == "attachment" and attachment_form.is_valid():
            attachment = attachment_form.save(commit=False)
            attachment.ticket = ticket
            attachment.save()
            AuditLog.objects.create(action="Ticket attachment uploaded", ticket=ticket, details=attachment.file.name)
            messages.success(request, "Attachment uploaded.")
            return redirect(ticket)

    return render(
        request,
        "tickets/ticket_detail.html",
        {
            "ticket": ticket,
            "status_form": status_form,
            "update_form": update_form,
            "attachment_form": attachment_form,
        },
    )


def knowledge_list(request):
    query = request.GET.get("q", "").strip()
    articles = KnowledgeArticle.objects.filter(published=True)
    if query:
        articles = articles.filter(Q(title__icontains=query) | Q(summary__icontains=query) | Q(content__icontains=query))
    return render(request, "tickets/knowledge_list.html", {"articles": articles, "query": query})


def knowledge_detail(request, pk):
    article = get_object_or_404(KnowledgeArticle, pk=pk, published=True)
    return render(request, "tickets/knowledge_detail.html", {"article": article})


def reports(request):
    by_status = Ticket.objects.values("status").annotate(total=Count("id"))
    by_category = Ticket.objects.values("category").annotate(total=Count("id"))
    by_department = Ticket.objects.values("department__name").annotate(total=Count("id"))
    return render(
        request,
        "tickets/reports.html",
        {
            "by_status": by_status,
            "by_category": by_category,
            "by_department": by_department,
        },
    )
