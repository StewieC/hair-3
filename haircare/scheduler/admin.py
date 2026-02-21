from django.contrib import admin
from .models import HairSchedule, ScheduleLog

@admin.register(HairSchedule)
class HairScheduleAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'event_type', 'custom_event_name', 'frequency', 'next_scheduled', 'reminder_enabled', 'is_active', 'created_at')
    list_filter = ('event_type', 'frequency', 'is_active', 'reminder_enabled', 'created_at')
    search_fields = ('session_id', 'custom_event_name', 'notes')
    list_editable = ('is_active',)
    readonly_fields = ('created_at',)

@admin.register(ScheduleLog)
class ScheduleLogAdmin(admin.ModelAdmin):
    list_display = ('schedule', 'completed_date', 'completed_time', 'mood', 'hair_condition')
    list_filter = ('completed_date', 'mood')
    search_fields = ('notes',)
    readonly_fields = ('completed_date', 'completed_time')