from django.db import models
from datetime import datetime, timedelta

class HairSchedule(models.Model):
    EVENT_TYPES = [
    ('wash', 'Wash Day'),
    ('deep_condition', 'Deep Conditioning'),
    ('protein_treatment', 'Protein Treatment'),
    ('trim', 'Trim/Haircut'),
    ('oil_treatment', 'Oil Treatment'),
    ('scalp_massage', 'Scalp Massage'),
    ('protective_style', 'Protective Styling'),
    ('clarifying_wash', 'Clarifying Wash'),
    ('retouch', 'Dreadlock/Locs Retouch'),  
    ('salon', 'Salon Appointment'),  
    ('color', 'Color/Dye Touch-up'),  
    ('relaxer', 'Relaxer/Perm'),  
    ('braids', 'Braids Installation'),  
    ('weave', 'Weave Installation'), 
    ('other', 'Other'),
]
    
    FREQUENCY_CHOICES = [
    ('daily', 'Daily'),
    ('every_2_days', 'Every 2 Days'),
    ('every_3_days', 'Every 3 Days'),
    ('weekly', 'Weekly'),
    ('biweekly', 'Every 2 Weeks'),
    ('monthly', 'Monthly (30 days)'),
    ('every_6_weeks', 'Every 6 Weeks'),  
    ('every_2_months', 'Every 2 Months (60 days)'),  
    ('every_3_months', 'Every 3 Months (90 days)'),  
    ('custom', 'Custom (specify days)'),
]
    
    DAYS_OF_WEEK = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]
    
    # User identification (session-based for now)
    session_id = models.CharField(max_length=100, db_index=True)
    
    # Event details
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    custom_event_name = models.CharField(max_length=100, blank=True, help_text="If event type is 'other'")
    
    # Scheduling
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    specific_day = models.CharField(max_length=20, choices=DAYS_OF_WEEK, blank=True, help_text="For weekly schedules")
    custom_interval_days = models.IntegerField(null=True, blank=True, help_text="For custom frequency")
    
    # Time
    time_of_day = models.TimeField(help_text="Preferred time for this event")
    
    # Reminders
    reminder_enabled = models.BooleanField(default=True)
    reminder_hours_before = models.IntegerField(default=2, help_text="Hours before event to send reminder")
    reminder_email = models.EmailField(blank=True, help_text="Email for reminders")
    
    # Tracking
    last_completed = models.DateField(null=True, blank=True)
    next_scheduled = models.DateField()
    
    # Notes
    notes = models.TextField(blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        event_name = self.custom_event_name if self.event_type == 'other' else self.get_event_type_display()
        return f"{event_name} - {self.get_frequency_display()}"
    
    def calculate_next_date(self):
        """Calculate next scheduled date based on frequency"""
        if not self.last_completed:
            return datetime.now().date()
        
        last_date = self.last_completed
        
        if self.frequency == 'daily':
            return last_date + timedelta(days=1)
        elif self.frequency == 'every_2_days':
            return last_date + timedelta(days=2)
        elif self.frequency == 'every_3_days':
            return last_date + timedelta(days=3)
        elif self.frequency == 'weekly':
            return last_date + timedelta(days=7)
        elif self.frequency == 'biweekly':
            return last_date + timedelta(days=14)
        elif self.frequency == 'monthly':
            return last_date + timedelta(days=30)
        elif self.frequency == 'every_6_weeks':  # NEW
            return last_date + timedelta(days=42)
        elif self.frequency == 'every_2_months':  # NEW
            return last_date + timedelta(days=60)
        elif self.frequency == 'every_3_months':  # NEW
            return last_date + timedelta(days=90)
        elif self.frequency == 'custom' and self.custom_interval_days:
            return last_date + timedelta(days=self.custom_interval_days)
        
        return last_date + timedelta(days=7)  # Default to weekly
    
    def mark_completed(self):
        """Mark event as completed and calculate next date"""
        self.last_completed = datetime.now().date()
        self.next_scheduled = self.calculate_next_date()
        self.save()
    
    class Meta:
        ordering = ['next_scheduled', 'time_of_day']


class ScheduleLog(models.Model):
    """Track completion history"""
    schedule = models.ForeignKey(HairSchedule, on_delete=models.CASCADE, related_name='logs')
    completed_date = models.DateField(auto_now_add=True)
    completed_time = models.TimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    mood = models.CharField(max_length=20, blank=True, choices=[
        ('great', '😊 Great'),
        ('good', '🙂 Good'),
        ('okay', '😐 Okay'),
        ('bad', '😕 Not Good'),
    ])
    hair_condition = models.IntegerField(null=True, blank=True, help_text="Rate 1-5")
    
    def __str__(self):
        return f"{self.schedule.get_event_type_display()} - {self.completed_date}"
    
    class Meta:
        ordering = ['-completed_date', '-completed_time']