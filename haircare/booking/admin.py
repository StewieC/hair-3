from django.contrib import admin
from django.utils import timezone
from .models import Hairdresser, Booking, StylistApplication

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


@admin.register(StylistApplication)
class StylistApplicationAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'owner_name', 'location', 'status', 'submitted_at')
    list_filter = ('status', 'location', 'submitted_at')
    search_fields = ('business_name', 'owner_name', 'email', 'phone')
    readonly_fields = ('submitted_at',)
    
    fieldsets = (
        ('Application Status', {
            'fields': ('status', 'admin_notes', 'approved_profile', 'reviewed_at')
        }),
        ('Business Information', {
            'fields': ('business_name', 'owner_name', 'email', 'phone')
        }),
        ('Location', {
            'fields': ('location', 'address')
        }),
        ('Services & Details', {
            'fields': ('services_offered', 'price_range', 'years_experience', 'business_hours', 'business_description')
        }),
        ('Portfolio', {
            'fields': ('portfolio_url', 'sample_work_url')
        }),
        ('Metadata', {
            'fields': ('submitted_at',)
        }),
    )
    
    actions = ['approve_applications', 'reject_applications']
    
    def approve_applications(self, request, queryset):
        for application in queryset.filter(status='pending'):
            # Create Hairdresser profile
            stylist = Hairdresser.objects.create(
                name=application.business_name,
                location=application.location,
                services=application.services_offered,
                price_range=application.price_range,
                phone=application.phone,
                available=True
            )
            
            # Update application
            application.status = 'approved'
            application.reviewed_at = timezone.now()
            application.approved_profile = stylist
            application.save()
        
        self.message_user(request, f"{queryset.count()} application(s) approved and stylist profiles created.")
    approve_applications.short_description = "Approve selected applications"
    
    def reject_applications(self, request, queryset):
        queryset.update(status='rejected', reviewed_at=timezone.now())
        self.message_user(request, f"{queryset.count()} application(s) rejected.")
    reject_applications.short_description = "Reject selected applications"