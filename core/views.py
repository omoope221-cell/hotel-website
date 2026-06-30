from django.shortcuts import render, redirect
from django.contrib import messages
from rooms.models import Room
from bookings.models import ContactMessage

def home(request):
    featured_rooms = Room.objects.filter(is_available=True)[:3]
    return render(request, 'core/home.html', {'featured_rooms': featured_rooms})

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    if request.method == 'POST':
        ContactMessage.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message'),
        )
        messages.success(request, 'Message sent successfully!')
        return redirect('contact')
    return render(request, 'core/contact.html')