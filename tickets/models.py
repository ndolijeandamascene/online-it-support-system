from django.conf import settings
from django.db import models
from django.urls import reverse


class Department(models.Model):
    name = models.CharField(max_length=120, unique=True)
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="managed_departments",
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    class Role(models.TextChoices):
        ADMINISTRATOR = "administrator", "Administrator"
        SUPPORT_STAFF = "support_staff", "IT Support Staff"
        DEPARTMENT_MANAGER = "department_manager", "Department Manager"
        EMPLOYEE = "employee", "Employee/Client"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=30, choices=Role.choices, default=Role.EMPLOYEE)
    department = models.ForeignKey(Department, blank=True, null=True, on_delete=models.SET_NULL)
    phone = models.CharField(max_length=40, blank=True)

    def __str__(self):
        return f"{self.user.get_username()} - {self.get_role_display()}"


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

    ticket_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    title = models.CharField(max_length=180)
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="requested_tickets",
    )
    requester_name = models.CharField(max_length=120)
    requester_email = models.EmailField()
    department = models.ForeignKey(Department, blank=True, null=True, on_delete=models.SET_NULL)
    department_name = models.CharField(max_length=100, blank=True)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="assigned_tickets",
    )
    category = models.CharField(max_length=30, choices=Category.choices, default=Category.OTHER)
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.MEDIUM)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    description = models.TextField()
    resolution_notes = models.TextField(blank=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    closed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.ticket_number or self.pk} {self.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.ticket_number:
            self.ticket_number = f"IT-{self.pk:06d}"
            super().save(update_fields=["ticket_number"])

    def get_absolute_url(self):
        return reverse("ticket_detail", kwargs={"pk": self.pk})


class TicketUpdate(models.Model):
    ticket = models.ForeignKey(Ticket, related_name="updates", on_delete=models.CASCADE)
    author = models.CharField(max_length=120, default="Support team")
    note = models.TextField()
    internal = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Update for ticket #{self.ticket_id}"


class TicketAttachment(models.Model):
    ticket = models.ForeignKey(Ticket, related_name="attachments", on_delete=models.CASCADE)
    file = models.FileField(upload_to="ticket_attachments/%Y/%m/")
    uploaded_by = models.CharField(max_length=120, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


class KnowledgeArticle(models.Model):
    title = models.CharField(max_length=180)
    category = models.CharField(max_length=30, choices=Ticket.Category.choices, default=Ticket.Category.OTHER)
    summary = models.CharField(max_length=240)
    content = models.TextField()
    published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("knowledge_detail", kwargs={"pk": self.pk})


class Asset(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        ASSIGNED = "assigned", "Assigned"
        MAINTENANCE = "maintenance", "Maintenance"
        RETIRED = "retired", "Retired"

    name = models.CharField(max_length=140)
    asset_tag = models.CharField(max_length=80, unique=True)
    serial_number = models.CharField(max_length=120, blank=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)
    department = models.ForeignKey(Department, blank=True, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    warranty_expires = models.DateField(blank=True, null=True)
    maintenance_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["asset_tag"]

    def __str__(self):
        return f"{self.asset_tag} - {self.name}"


class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, blank=True, null=True, on_delete=models.CASCADE)
    message = models.CharField(max_length=240)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.message


class AuditLog(models.Model):
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=120)
    ticket = models.ForeignKey(Ticket, blank=True, null=True, on_delete=models.SET_NULL)
    details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.action
