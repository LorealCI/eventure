from django.db import models
from django.contrib.auth.models import User
from datetime import date
from cloudinary.models import CloudinaryField


# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=255)
    event_date = models.DateField(default=date.today)
    start_time = models.TimeField(default="00:00")
    end_time = models.TimeField(default="00:00")
    organiser = models.ForeignKey(User, related_name='events', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    max_capacity = models.PositiveIntegerField(default=50)
    image = CloudinaryField('image', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    age_rating = models.CharField(
        max_length=20,
        choices=[
            ('All Ages', 'All Ages'),
            ('5+', '5+'),
            ('8+', '8+'),
            ('13+', '13+'),
            ('18+', '18+'),
        ],
        default='All Ages'
    )

    def spaces_left(self):
        # Counts the number of RSVPs for this event.
        rsvp_count = self.rsvps.count()
        return self.max_capacity - rsvp_count

    def is_full(self):
        # Checks if the event has no spaces left.
        return self.spaces_left() <= 0

    def __str__(self):
        return self.title


class Meta:
    ordering = ["-event_time"]


class RSVP(models.Model):
    user = models.ForeignKey(User, related_name='rsvps', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='rsvps', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('Yes', 'Yes')], default='Yes')
    rsvp_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} RSVP to {self.event.title} ({self.status})"
