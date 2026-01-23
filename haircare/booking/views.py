from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Hairdresser, Booking

def stylist_list(request):
    location = request.GET.get('location', '')
    if location:
        stylists = Hairdresser.objects.filter(location__icontains=location)
    else:
        stylists = Hairdresser.objects.all()
    
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