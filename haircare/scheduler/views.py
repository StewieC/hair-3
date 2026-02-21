from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import datetime, date, timedelta
from .models import HairSchedule, ScheduleLog
import calendar

def get_or_create_session_id(request):
    """Get or create session ID for user"""
    if 'schedule_session_id' not in request.session:
        request.session['schedule_session_id'] = f"session_{datetime.now().timestamp()}"
    return request.session['schedule_session_id']


def calendar_home(request):
    """Display calendar view with scheduled events"""
    session_id = get_or_create_session_id(request)
    
    # Get current month/year or from query params
    today = date.today()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))
    
    # Get all schedules for this user
    schedules = HairSchedule.objects.filter(session_id=session_id, is_active=True)
    
    # Get events for this month
    first_day = date(year, month, 1)
    last_day = date(year, month, calendar.monthrange(year, month)[1])
    
    # Build calendar data
    cal = calendar.monthcalendar(year, month)
    
    # Get events happening this month
    events_by_date = {}
    for schedule in schedules:
        if first_day <= schedule.next_scheduled <= last_day:
            date_key = schedule.next_scheduled.day
            if date_key not in events_by_date:
                events_by_date[date_key] = []
            events_by_date[date_key].append(schedule)
    
    # Get today's events
    today_events = schedules.filter(next_scheduled=today)
    upcoming_events = schedules.filter(next_scheduled__gt=today, next_scheduled__lte=today + timedelta(days=7))
    
    # Navigation dates
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1
    
    context = {
        'schedules': schedules,
        'today_events': today_events,
        'upcoming_events': upcoming_events,
        'calendar': cal,
        'events_by_date': events_by_date,
        'year': year,
        'month': month,
        'month_name': calendar.month_name[month],
        'today': today,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
    }
    return render(request, 'scheduler/calendar_home.html', context)


def add_schedule(request):
    """Add new schedule"""
    session_id = get_or_create_session_id(request)
    
    if request.method == 'POST':
        # Get form data
        event_type = request.POST.get('event_type')
        custom_event_name = request.POST.get('custom_event_name', '')
        frequency = request.POST.get('frequency')
        specific_day = request.POST.get('specific_day', '')
        custom_interval_days = request.POST.get('custom_interval_days')
        time_of_day = request.POST.get('time_of_day')
        reminder_enabled = request.POST.get('reminder_enabled') == 'on'
        reminder_hours_before = int(request.POST.get('reminder_hours_before', 2))
        reminder_email = request.POST.get('reminder_email', '')
        notes = request.POST.get('notes', '')
        
        # Create schedule
        schedule = HairSchedule.objects.create(
            session_id=session_id,
            event_type=event_type,
            custom_event_name=custom_event_name,
            frequency=frequency,
            specific_day=specific_day,
            custom_interval_days=int(custom_interval_days) if custom_interval_days else None,
            time_of_day=time_of_day,
            reminder_enabled=reminder_enabled,
            reminder_hours_before=reminder_hours_before,
            reminder_email=reminder_email,
            notes=notes,
            next_scheduled=date.today(),  # Start from today
        )
        
        messages.success(request, f"✅ {schedule} has been added to your calendar!")
        return redirect('calendar_home')
    
    context = {
        'event_types': HairSchedule.EVENT_TYPES,
        'frequencies': HairSchedule.FREQUENCY_CHOICES,
        'days_of_week': HairSchedule.DAYS_OF_WEEK,
    }
    return render(request, 'scheduler/add_schedule.html', context)


def edit_schedule(request, schedule_id):
    """Edit existing schedule"""
    session_id = get_or_create_session_id(request)
    schedule = get_object_or_404(HairSchedule, id=schedule_id, session_id=session_id)
    
    if request.method == 'POST':
        schedule.event_type = request.POST.get('event_type')
        schedule.custom_event_name = request.POST.get('custom_event_name', '')
        schedule.frequency = request.POST.get('frequency')
        schedule.specific_day = request.POST.get('specific_day', '')
        schedule.custom_interval_days = int(request.POST.get('custom_interval_days')) if request.POST.get('custom_interval_days') else None
        schedule.time_of_day = request.POST.get('time_of_day')
        schedule.reminder_enabled = request.POST.get('reminder_enabled') == 'on'
        schedule.reminder_hours_before = int(request.POST.get('reminder_hours_before', 2))
        schedule.reminder_email = request.POST.get('reminder_email', '')
        schedule.notes = request.POST.get('notes', '')
        schedule.save()
        
        messages.success(request, "Schedule updated!")
        return redirect('calendar_home')
    
    context = {
        'schedule': schedule,
        'event_types': HairSchedule.EVENT_TYPES,
        'frequencies': HairSchedule.FREQUENCY_CHOICES,
        'days_of_week': HairSchedule.DAYS_OF_WEEK,
    }
    return render(request, 'scheduler/edit_schedule.html', context)


def delete_schedule(request, schedule_id):
    """Delete schedule"""
    session_id = get_or_create_session_id(request)
    schedule = get_object_or_404(HairSchedule, id=schedule_id, session_id=session_id)
    schedule.delete()
    messages.success(request, "Schedule deleted!")
    return redirect('calendar_home')


def mark_completed(request, schedule_id):
    """Mark event as completed"""
    session_id = get_or_create_session_id(request)
    schedule = get_object_or_404(HairSchedule, id=schedule_id, session_id=session_id)
    
    if request.method == 'POST':
        # Create log entry
        ScheduleLog.objects.create(
            schedule=schedule,
            notes=request.POST.get('notes', ''),
            mood=request.POST.get('mood', ''),
            hair_condition=int(request.POST.get('hair_condition')) if request.POST.get('hair_condition') else None,
        )
        
        # Update schedule
        schedule.mark_completed()
        
        messages.success(request, f"✅ {schedule} marked as completed! Next scheduled: {schedule.next_scheduled}")
        return redirect('calendar_home')
    
    return render(request, 'scheduler/mark_completed.html', {'schedule': schedule})


def schedule_history(request):
    """View completion history"""
    session_id = get_or_create_session_id(request)
    schedules = HairSchedule.objects.filter(session_id=session_id)
    
    # Get all logs
    logs = ScheduleLog.objects.filter(schedule__session_id=session_id).order_by('-completed_date')[:50]
    
    # Calculate streaks and stats
    total_completed = logs.count()
    this_week = logs.filter(completed_date__gte=date.today() - timedelta(days=7)).count()
    this_month = logs.filter(completed_date__gte=date.today() - timedelta(days=30)).count()
    
    context = {
        'logs': logs,
        'schedules': schedules,
        'total_completed': total_completed,
        'this_week': this_week,
        'this_month': this_month,
    }
    return render(request, 'scheduler/history.html', context)