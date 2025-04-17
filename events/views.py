from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Event, EventCategory
from .forms import EventForm, EventCategoryForm
from django.utils import timezone

def home(request):
    upcoming_events = Event.objects.filter(
        status='published',
        date__gt=timezone.now()
    ).order_by('date')[:6]
    
    context = {
        'upcoming_events': upcoming_events,
    }
    return render(request, 'events/home.html', context)

def event_list(request):
    events = Event.objects.filter(status='published').order_by('-date')
    
    # Filtering
    category = request.GET.get('category')
    if category:
        events = events.filter(category__name=category)
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        events = events.filter(title__icontains=search_query)
    
    # Pagination
    paginator = Paginator(events, 6)  # Show 6 events per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = EventCategory.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': category,
        'search_query': search_query,
    }
    return render(request, 'events/event_list.html', context)

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    is_attending = False
    if request.user.is_authenticated:
        is_attending = request.user in event.attendees.all()
    
    context = {
        'event': event,
        'is_attending': is_attending,
    }
    return render(request, 'events/event_detail.html', context)

@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('events:event_detail', pk=event.pk)
    else:
        form = EventForm()
    
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Create Event'})

@login_required
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.user != event.organizer:
        messages.error(request, "You don't have permission to edit this event.")
        return redirect('events:event_detail', pk=event.pk)
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('events:event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Update Event'})

@login_required 
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.user != event.organizer:
        messages.error(request, "You don't have permission to delete this event.")
        return redirect('events:event_detail', pk=event.pk)
    
    if request.method == 'GET':
        return render(request, 'events/event_confirm_delete.html', {'event': event})
    
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('events:event_list')
    
    return redirect('events:event_detail', pk=event.pk)

@login_required
def toggle_attendance(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.user in event.attendees.all():
        event.attendees.remove(request.user)
        messages.success(request, "You're no longer attending this event.")
    else:
        if event.capacity > 0 and event.attendees.count() >= event.capacity:
            messages.error(request, "This event has reached its capacity.")
        else:
            event.attendees.add(request.user)
            messages.success(request, "You're now attending this event!")
    
    return redirect('events:event_detail', pk=event.pk)

@login_required
def my_events(request):
    organized_events = request.user.organized_events.all()
    attended_events = request.user.attended_events.all()
    
    context = {
        'organized_events': organized_events,
        'attended_events': attended_events,
    }
    return render(request, 'events/my_events.html', context)