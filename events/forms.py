from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['is_active', 'organiser']
        fields = ['image', 'title', 'description', 'location', 'event_date', 'start_time', 'end_time', 'max_capacity', 'age_rating']
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Start typing a location...',
                'id': 'location',  # Add an ID for JavaScript integration
                'autocomplete': 'on',  # Disable browser's default autocomplete
            }),
        }

    def clean_event_date(self):
        event_date = self.cleaned_data.get('event_date')
        if event_date < date.today():
            raise ValidationError("The event date cannot be in the past.")
        return event_date

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time and start_time >= end_time:
            raise ValidationError("End time must be after start time.")
        return cleaned_data
