from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Sum, Count
from django.utils import timezone
from rooms.models import Room, Amenity
from bookings.models import Booking, ContactMessage
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def dashboard_home(request):
    today = timezone.now().date()
    
    context = {
        'total_rooms': Room.objects.count(),
        'available_rooms': Room.objects.filter(is_available=True).count(),
        'total_bookings': Booking.objects.count(),
        'pending_bookings': Booking.objects.filter(status='pending').count(),
        'confirmed_bookings': Booking.objects.filter(status='confirmed').count(),
        'today_checkins': Booking.objects.filter(check_in=today, status='confirmed').count(),
        'today_checkouts': Booking.objects.filter(check_out=today, status='checked_in').count(),
        'total_revenue': Booking.objects.filter(status__in=['confirmed', 'checked_in', 'checked_out']).aggregate(Sum('total_price'))['total_price__sum'] or 0,
        'recent_bookings': Booking.objects.select_related('room').order_by('-created_at')[:10],
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
    }
    return render(request, 'dashboard/home.html', context)


@staff_member_required
def bookings_list(request):
    bookings = Booking.objects.select_related('room').order_by('-created_at')
    status = request.GET.get('status')
    if status:
        bookings = bookings.filter(status=status)
    return render(request, 'dashboard/bookings.html', {'bookings': bookings})


@staff_member_required
def booking_update(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        booking.status = request.POST.get('status')
        booking.save()
        messages.success(request, 'Booking updated.')
        return redirect('dashboard:bookings')
    return render(request, 'dashboard/booking_form.html', {'booking': booking})


@staff_member_required
def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, f'Booking for {booking.guest_name} has been deleted.')
        return redirect('dashboard:bookings')
    return render(request, 'dashboard/booking_confirm_delete.html', {'booking': booking})


@staff_member_required
def rooms_manage(request):
    rooms = Room.objects.all()
    return render(request, 'dashboard/rooms.html', {'rooms': rooms})


@staff_member_required
def room_add(request):
    amenities = Amenity.objects.all()
    if request.method == 'POST':
        room = Room.objects.create(
            name=request.POST.get('name'),
            room_type=request.POST.get('room_type'),
            price_per_night=request.POST.get('price_per_night'),
            capacity=request.POST.get('capacity'),
            size_sqm=request.POST.get('size_sqm'),
            description=request.POST.get('description'),
            total_rooms=request.POST.get('total_rooms'),
            is_available=request.POST.get('is_available') == 'on',
        )
        
        # Handle amenities
        amenity_ids = request.POST.getlist('amenities')
        if amenity_ids:
            room.amenities.set(amenity_ids)
        
        # Handle image upload
        if request.FILES.get('image'):
            room.image = request.FILES['image']
            room.save()
        
        messages.success(request, f'Room "{room.name}" added successfully!')
        return redirect('dashboard:rooms')
    
    return render(request, 'dashboard/room_form.html', {'amenities': amenities, 'room': None})


@staff_member_required
def room_edit(request, pk):
    room = get_object_or_404(Room, pk=pk)
    amenities = Amenity.objects.all()
    
    if request.method == 'POST':
        room.name = request.POST.get('name')
        room.room_type = request.POST.get('room_type')
        room.price_per_night = request.POST.get('price_per_night')
        room.capacity = request.POST.get('capacity')
        room.size_sqm = request.POST.get('size_sqm')
        room.description = request.POST.get('description')
        room.total_rooms = request.POST.get('total_rooms')
        room.is_available = request.POST.get('is_available') == 'on'
        
        # Handle amenities
        amenity_ids = request.POST.getlist('amenities')
        if amenity_ids:
            room.amenities.set(amenity_ids)
        else:
            room.amenities.clear()
        
        # Handle image upload
        if request.FILES.get('image'):
            room.image = request.FILES['image']
        
        room.save()
        messages.success(request, f'Room "{room.name}" updated successfully!')
        return redirect('dashboard:rooms')
    
    return render(request, 'dashboard/room_form.html', {'amenities': amenities, 'room': room})


@staff_member_required
def room_delete(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room_name = room.name
        room.delete()
        messages.success(request, f'Room "{room_name}" deleted successfully!')
        return redirect('dashboard:rooms')
    return render(request, 'dashboard/room_confirm_delete.html', {'room': room})


@staff_member_required
def messages_list(request):
    msgs = ContactMessage.objects.order_by('-created_at')
    return render(request, 'dashboard/messages.html', {'messages': msgs})


@staff_member_required
def message_read(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    msg.is_read = True
    msg.save()
    return render(request, 'dashboard/message_detail.html', {'msg': msg})

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

def dashboard_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard:home')
        else:
            messages.error(request, 'Invalid username or password, or you are not a staff member.')
    
    return render(request, 'dashboard/login.html')

def dashboard_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('dashboard:login')