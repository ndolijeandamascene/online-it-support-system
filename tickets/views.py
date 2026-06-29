from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import TicketForm, TicketStatusForm, TicketUpdateForm
from .models import Ticket


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


@require_http_methods(["GET", "POST"])
def ticket_create(request):
    form = TicketForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        ticket = form.save()
        messages.success(request, "Support ticket created successfully.")
        return redirect(ticket)

    return render(request, "tickets/ticket_form.html", {"form": form})


@require_http_methods(["GET", "POST"])
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    status_form = TicketStatusForm(request.POST or None, instance=ticket, prefix="status")
    update_form = TicketUpdateForm(request.POST or None, prefix="update")

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "status" and status_form.is_valid():
            status_form.save()
            messages.success(request, "Ticket status updated.")
            return redirect(ticket)
        if action == "note" and update_form.is_valid():
            note = update_form.save(commit=False)
            note.ticket = ticket
            note.save()
            messages.success(request, "Update added to the ticket.")
            return redirect(ticket)

    return render(
        request,
        "tickets/ticket_detail.html",
        {"ticket": ticket, "status_form": status_form, "update_form": update_form},
    )

# Create your views here.
