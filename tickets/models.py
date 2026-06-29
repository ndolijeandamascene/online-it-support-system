from django.db import models
from django.urls import reverse


class Ticket(models.Model):
    class Category(models.TextChoices):
        HARDWARE = "hardware", "Hardware"
        SOFTWARE = "software", "Software"
        NETWORK = "network", "Network"
        EMAIL = "email", "Email"
        SECURITY = "security", "Security"
        OTHER = "other", "Other"

    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        URGENT = "urgent", "Urgent"

    class Status(models.TextChoices):
        OPEN = "open", "Open"
        IN_PROGRESS = "in_progress", "In progress"
        WAITING = "waiting", "Waiting for user"
        RESOLVED = "resolved", "Resolved"
        CLOSED = "closed", "Closed"

    title = models.CharField(max_length=180)
    requester_name = models.CharField(max_length=120)
    requester_email = models.EmailField()
    department = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=30, choices=Category.choices, default=Category.OTHER)
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.MEDIUM)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"#{self.pk} {self.title}"

    def get_absolute_url(self):
        return reverse("ticket_detail", kwargs={"pk": self.pk})


class TicketUpdate(models.Model):
    ticket = models.ForeignKey(Ticket, related_name="updates", on_delete=models.CASCADE)
    author = models.CharField(max_length=120, default="Support team")
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Update for ticket #{self.ticket_id}"

# Create your models here.
