from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
import requests
from django.http import JsonResponse
from django.contrib import messages
from .models import Event, RSVP
from .forms import EventForm  # Form for creating events


# Create your views here.
# View to display all the events (index page).
def event_list(request):
    events = Event.objects.filter(is_active=True).order_by('event_time')  # Shows the active events.
    return render(request, 'events/event_list.html', {'events': events})


# View to display the details of a individual event.
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Retrieve RSVPs for the event to check if the current user is attending.
    user_rsvp = None
    if request.user.is_authenticated:
        user_rsvp = RSVP.objects.filter(user=request.user, event=event).first()

    return render(request, 'events/event_detail.html', {
        'event': event,
        'user_rsvp': user_rsvp,
    })


# View to handle user RSVPs to an event.
@login_required
def attend_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Checks if the event is full.
    if event.is_full():
        messages.error(request, 'Sorry, this event is fully booked.')
        return redirect('event_detail', event_id=event.id)

    # Checks if the user is already attending.
    if RSVP.objects.filter(user=request.user, event=event).exists():
        messages.info(request, 'You are already attending this event.')
        return redirect('event_detail', event_id=event.id)

    # Creates an RSVP for the user.
    RSVP.objects.create(user=request.user, event=event, status='Yes')
    messages.success(request, 'You are now attending this event!')
    return redirect('event_detail', event_id=event.id)


# Checks for event organiser.
def is_event_organiser(user):
    return user.groups.filter(name='Event Organisers').exists() or user.is_staff


# View to create a new event via admin or event organiser.
@login_required
@user_passes_test(is_event_organiser, login_url='event_list')
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organiser = request.user  # Set the logged-in user as the organiser
            event.is_active = True  # Set the event as active
            event.save()
            messages.success(request, 'Event created successfully!')  # Add success message
            return redirect('create_event')  # Redirect to the same page to reset the form
    else:
        form = EventForm()

    return render(request, 'events/create_event.html', {'form': form})


# View to update an existing event (only for the event organiser).
@login_required
def update_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Ensures the logged-in user is the event organiser.
    if event.organiser != request.user:
        messages.error(request, 'You do not have permission to edit this event.')
        return redirect('event_list')

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)

    return render(request, 'events/update_event.html', {'form': form, 'event': event})


# View to delete an event (only for the event organiser).
@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Ensure the logged-in user is the event organiser.
    if event.organiser != request.user:
        messages.error(request, 'You do not have permission to delete this event.')
        return redirect('event_list')

    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('event_list')

    return render(request, 'events/delete_event.html', {'event': event})


def location_autocomplete(request):
    query = request.GET.get('q', '')  # Get the query from the request
    if query:
        # Use Nominatim API to fetch location data
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': query,
            'countrycodes': 'gb',  # Limit to Great Britain (England, Scotland, Wales)
            'addressdetails': 1,
            'format': 'json',
            'limit': 5,  # Limit the number of results
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            # Extract street names or postcodes from the response
            suggestions = [
                f"{item['address'].get('road', '')}, {item['address'].get('postcode', '')}".strip(', ')
                for item in data
                if 'road' in item['address'] or 'postcode' in item['address']
            ]
        else:
            suggestions = []
    else:
        suggestions = []

    return JsonResponse({'suggestions': suggestions})