from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
from django.http import JsonResponse
from django.contrib import messages
from .models import Event, RSVP
from .forms import EventForm  


# Create your views here.
# View to display the home page.
def home(request):
    # Get a few featured events to display.
    featured_events = Event.objects.filter(is_featured=True, is_active=True)[:4]  # Adjust as needed
    return render(request, 'events/home.html', {'featured_events': featured_events})


# View to display all events.
def event_list(request):
    events = Event.objects.filter(is_active=True).order_by('start_time')  # Shows the active events.
    paginator = Paginator(events, 8)  # Show 8 events per page

    page = request.GET.get('page')  # Get the page number from the query parameters
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)  # If page is not an integer, deliver the first page
    except EmptyPage:
        events = paginator.page(paginator.num_pages)  # If page is out of range, deliver the last page

    return render(request, 'events/event_list.html', {'events': events})


def about(request):
    return render(request, 'events/about.html')


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
        form = EventForm(request.POST, request.FILES)
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
        form = EventForm(request.POST, request.FILES, instance=event)
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
