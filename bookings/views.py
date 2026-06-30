from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import datetime
from rooms.models import Room
from .models import Booking

def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        check_in_str = request.POST.get('check_in')
        check_out_str = request.POST.get('check_out')
        
        if check_in_str and check_out_str:
            # Convert strings to date objects
            check_in = datetime.strptime(check_in_str, '%Y-%m-%d').date()
            check_out = datetime.strptime(check_out_str, '%Y-%m-%d').date()
            
            Booking.objects.create(
                guest_name=request.POST.get('name'),
                guest_email=request.POST.get('email'),
                guest_phone=request.POST.get('phone'),
                user=request.user if request.user.is_authenticated else None,
                room=room,
                check_in=check_in,
                check_out=check_out,
                adults=int(request.POST.get('adults', 1)),
                children=int(request.POST.get('children', 0)),
                special_requests=request.POST.get('special_requests', ''),
            )
            messages.success(request, 'Booking submitted! We will confirm shortly.')
            return redirect('booking_success')
    return render(request, 'bookings/book.html', {'room': room})

def booking_success(request):
    return render(request, 'bookings/success.html')