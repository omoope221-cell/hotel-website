from django.shortcuts import render, get_object_or_404
from .models import Room

def room_list(request):
    rooms = Room.objects.filter(is_available=True)
    room_type = request.GET.get('type')
    if room_type:
        rooms = rooms.filter(room_type=room_type)
    return render(request, 'rooms/list.html', {'rooms': rooms})

def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    return render(request, 'rooms/detail.html', {'room': room})