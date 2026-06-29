from django.test import TestCase
from django.urls import reverse

from .models import Ticket, TicketUpdate


class TicketViewsTests(TestCase):
    def test_ticket_list_loads(self):
        response = self.client.get(reverse("ticket_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Support tickets")

    def test_create_ticket(self):
        response = self.client.post(
            reverse("ticket_create"),
            {
                "title": "Laptop cannot connect to Wi-Fi",
                "requester_name": "Aline Mugisha",
                "requester_email": "aline@example.com",
                "department": "Finance",
                "category": Ticket.Category.NETWORK,
                "priority": Ticket.Priority.HIGH,
                "description": "The laptop drops from the office Wi-Fi every few minutes.",
            },
        )

        ticket = Ticket.objects.get()
        self.assertRedirects(response, ticket.get_absolute_url())
        self.assertEqual(ticket.status, Ticket.Status.OPEN)

    def test_ticket_detail_adds_note(self):
        ticket = Ticket.objects.create(
            title="Printer queue stuck",
            requester_name="Jean Ndoli",
            requester_email="jean@example.com",
            category=Ticket.Category.HARDWARE,
            priority=Ticket.Priority.MEDIUM,
            description="Shared printer queue is not processing documents.",
        )

        response = self.client.post(
            ticket.get_absolute_url(),
            {
                "action": "note",
                "update-author": "Help desk",
                "update-note": "Restarted print spooler and asked user to retest.",
                "status-status": ticket.status,
                "status-priority": ticket.priority,
            },
        )

        self.assertRedirects(response, ticket.get_absolute_url())
        self.assertEqual(TicketUpdate.objects.count(), 1)

    def test_ticket_detail_updates_status(self):
        ticket = Ticket.objects.create(
            title="Email password reset",
            requester_name="Grace",
            requester_email="grace@example.com",
            category=Ticket.Category.EMAIL,
            priority=Ticket.Priority.LOW,
            description="User cannot sign in to email.",
        )

        response = self.client.post(
            ticket.get_absolute_url(),
            {
                "action": "status",
                "status-status": Ticket.Status.RESOLVED,
                "status-priority": Ticket.Priority.MEDIUM,
                "update-author": "Help desk",
                "update-note": "",
            },
        )

        ticket.refresh_from_db()
        self.assertRedirects(response, ticket.get_absolute_url())
        self.assertEqual(ticket.status, Ticket.Status.RESOLVED)
        self.assertEqual(ticket.priority, Ticket.Priority.MEDIUM)

# Create your tests here.
