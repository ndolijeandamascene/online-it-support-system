from django import forms

from .models import Ticket, TicketUpdate


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
        fields = ["status", "priority"]


class TicketUpdateForm(forms.ModelForm):
    class Meta:
        model = TicketUpdate
        fields = ["author", "note"]
        widgets = {
            "note": forms.Textarea(attrs={"rows": 3}),
        }
