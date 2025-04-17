from django import forms
from .models import Event, EventCategory
from django.contrib.auth import get_user_model

User = get_user_model()

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title', 'description', 'date', 'location', 
            'category', 'image', 'status', 'capacity',
            'registration_deadline'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter a clear, descriptive title'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Describe your event in detail'
            }),
            'location': forms.TextInput(attrs={
                'placeholder': 'Enter the full address or venue name'
            }),
            'date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'registration_deadline': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'capacity': forms.NumberInput(attrs={
                'placeholder': '0 for unlimited',
                'min': '0'
            }),
        }
        help_texts = {
            'title': 'Choose a title that clearly describes your event (max 200 characters)',
            'description': 'Include important details like schedule, what to bring, etc.',
            'capacity': 'Set to 0 for unlimited attendance',
            'registration_deadline': 'Must be before the event date',
            'image': 'Recommended size: 800x600px or larger',
        }

class EventCategoryForm(forms.ModelForm):
    class Meta:
        model = EventCategory
        fields = ['name', 'description']