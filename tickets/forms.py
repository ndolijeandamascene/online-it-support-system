from django import forms

from .models import Ticket, TicketAttachment, TicketUpdate


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            "title",
            "requester_name",
            "requester_email",
            "department",
            "category",
            "priority",
            "description",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
        }


class TicketStatusForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["assigned_to", "status", "priority", "resolution_notes"]
        widgets = {
            "resolution_notes": forms.Textarea(attrs={"rows": 3}),
        }


class TicketUpdateForm(forms.ModelForm):
    class Meta:
        model = TicketUpdate
        fields = ["author", "note", "internal"]
        widgets = {
            "note": forms.Textarea(attrs={"rows": 3}),
        }


class TicketAttachmentForm(forms.ModelForm):
    class Meta:
        model = TicketAttachment
        fields = ["file", "uploaded_by"]
