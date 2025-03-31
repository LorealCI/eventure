from . import views
from django.urls import path

urlpatterns = [
  path('', views.home, name='home'),  # Home page
  path('event/', views.event_list, name='event_list'),
  path('about/', views.about, name='about'),
  path('event/<int:event_id>/', views.event_detail, name='event_detail'),  # Event detail page
  path('event/<int:event_id>/attend/', views.attend_event, name='event_attend'),  # RSVP for event
  path('event/create/', views.create_event, name='create_event'),  # Create event
  path('event/<int:event_id>/update/', views.update_event, name='update_event'),  # Update event
  path('event/<int:event_id>/delete/', views.delete_event, name='delete_event'),  # Delete event
]