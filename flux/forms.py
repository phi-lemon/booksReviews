from django import forms
from .models import Ticket
from django.contrib.auth.models import User


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ("title", "description", "upload", "user")
        widgets = {'user': forms.HiddenInput()}

