from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'event_date', 'event_time', 'max_capacity']
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
            'event_time': forms.TimeInput(attrs={'type': 'time'}),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Start typing a location...',
                'id': 'location',  # Add an ID for JavaScript integration
                'autocomplete': 'off',  # Disable browser's default autocomplete
            }),
        }

    def clean_event_date(self):
        event_date = self.cleaned_data.get('event_date')
        if event_date < date.today():
            raise ValidationError("The event date cannot be in the past.")
        return event_date
    