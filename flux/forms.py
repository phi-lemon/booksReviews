from django import forms
from .models import Ticket, Review


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]
        widgets = {'description': forms.Textarea}


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["headline", "body", "rating"]
        widgets = {'body': forms.Textarea}
