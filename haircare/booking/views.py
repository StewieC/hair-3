from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Hairdresser, Booking, StylistApplication

def stylist_list(request):
    location = request.GET.get('location', '')
    if location:
        stylists = Hairdresser.objects.filter(location__icontains=location, available=True)
    else:
        stylists = Hairdresser.objects.filter(available=True)
    
    return render(request, 'booking/stylist_list.html', {
        'stylists': stylists,
        'current_location': location
    })


def book_stylist(request, stylist_id):
    stylist = get_object_or_404(Hairdresser, id=stylist_id)
    
    if request.method == 'POST':
        Booking.objects.create(
            client_name=request.POST['client_name'],
            client_phone=request.POST['client_phone'],
            hairdresser=stylist,
            service=request.POST['service'],
            date=request.POST['date'],
            time=request.POST['time'],
            notes=request.POST.get('notes', '')
        )
        messages.success(request, f"Booking confirmed with {stylist.name}!")
        return redirect('stylist_list')
    
    return render(request, 'booking/book_form.html', {'stylist': stylist})


# NEW VIEW: Stylist Registration Form
def register_stylist(request):
    if request.method == 'POST':
        application = StylistApplication.objects.create(
            business_name=request.POST.get('business_name'),
            owner_name=request.POST.get('owner_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            location=request.POST.get('location'),
            address=request.POST.get('address'),
            services_offered=request.POST.get('services_offered'),
            price_range=request.POST.get('price_range'),
            years_experience=int(request.POST.get('years_experience', 0)),
            portfolio_url=request.POST.get('portfolio_url', ''),
            sample_work_url=request.POST.get('sample_work_url', ''),
            business_description=request.POST.get('business_description'),
            business_hours=request.POST.get('business_hours'),
        )
        
        messages.success(request, "Application submitted successfully! We'll review it and contact you within 48 hours.")
        return redirect('application_success')
    
    return render(request, 'booking/register_stylist.html')


# NEW VIEW: Application Success Page
def application_success(request):
    return render(request, 'booking/application_success.html')


# NEW VIEW: Check Application Status
def check_application(request):
    application = None
    
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        
        # Find application by email and phone
        try:
            application = StylistApplication.objects.get(email=email, phone=phone)
        except StylistApplication.DoesNotExist:
            messages.error(request, "No application found with those details.")
    
    return render(request, 'booking/check_application.html', {'application': application})