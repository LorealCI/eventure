"""
URL configuration for eventure project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from events import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.event_list, name='event_list'),  # Event list page
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),  # Event detail page
    path('event/<int:event_id>/attend/', views.attend_event, name='event_attend'),  # RSVP for event
    path('event/create/', views.create_event, name='create_event'),  # Create event
    path('event/<int:event_id>/update/', views.update_event, name='update_event'),  # Update event
    path('event/<int:event_id>/delete/', views.delete_event, name='delete_event'),  # Delete event

]
