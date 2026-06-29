from django import forms
from django.contrib.auth import get_user_model

from .models import Ticket, TicketAttachment, TicketUpdate, UserProfile


class BootstrapFormMixin:
    def _apply_bootstrap_classes(self):
        for field in self.fields.values():
            widget = field.widget
            css_class = "form-check-input" if isinstance(widget, forms.CheckboxInput) else "form-control"
            if isinstance(widget, forms.Select):
                css_class = "form-select"
            existing = widget.attrs.get("class", "")
            widget.attrs["class"] = f"{existing} {css_class}".strip()


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        BootstrapFormMixin._apply_bootstrap_classes(self)


class TicketStatusForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["assigned_to", "status", "priority", "resolution_notes"]
        widgets = {
            "resolution_notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        BootstrapFormMixin._apply_bootstrap_classes(self)


class TicketUpdateForm(forms.ModelForm):
    class Meta:
        model = TicketUpdate
        fields = ["author", "note", "internal"]
        widgets = {
            "note": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        BootstrapFormMixin._apply_bootstrap_classes(self)


class TicketAttachmentForm(forms.ModelForm):
    class Meta:
        model = TicketAttachment
        fields = ["file", "uploaded_by"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        BootstrapFormMixin._apply_bootstrap_classes(self)


class UserAccountForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        BootstrapFormMixin._apply_bootstrap_classes(self)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["department", "phone"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        BootstrapFormMixin._apply_bootstrap_classes(self)
