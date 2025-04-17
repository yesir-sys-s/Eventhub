from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

User = get_user_model()

class EventCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('cancelled', 'Cancelled'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    category = models.ForeignKey(EventCategory, on_delete=models.SET_NULL, null=True, blank=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    attendees = models.ManyToManyField(User, related_name='attended_events', blank=True)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    capacity = models.PositiveIntegerField(default=0)
    registration_deadline = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('events:event_detail', args=[str(self.id)])

    def is_upcoming(self):
        return self.date > timezone.now()

    def available_seats(self):
        if self.capacity == 0:
            return "Unlimited"
        return self.capacity - self.attendees.count()

    def get_event_state(self):
        now = timezone.now()
        if self.status == 'cancelled':
            return 'cancelled'
        elif self.date < now:
            return 'finished'
        elif self.registration_deadline and self.registration_deadline < now:
            return 'registration_closed'
        elif self.capacity > 0 and self.attendees.count() >= self.capacity:
            return 'full'
        return 'open'