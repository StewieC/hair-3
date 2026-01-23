from django.contrib import admin
from .models import Hairdresser, Booking

@admin.register(Hairdresser)
class HairdresserAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'phone', 'rating', 'available')
    list_filter = ('location', 'available')
    search_fields = ('name', 'location', 'services')
    list_editable = ('available',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'hairdresser', 'service', 'date', 'time', 'created_at')
    list_filter = ('date', 'created_at')
    search_fields = ('client_name', 'client_phone', 'service')
    readonly_fields = ('created_at',)