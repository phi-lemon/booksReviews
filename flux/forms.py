from django import forms
from .models import Ticket, Review
from django.contrib.auth.models import User


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image", "user"]
        widgets = {'description': forms.Textarea, 'user': forms.HiddenInput()}


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["headline", "body", "rating", "user", "ticket"]
        # widgets = {'body': forms.Textarea, 'user': forms.HiddenInput()}
        widgets = {'body': forms.Textarea, 'user': forms.HiddenInput(), 'ticket': forms.HiddenInput()}

