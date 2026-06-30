# rooms/admin.py
from django.contrib import admin
from .models import Room, Amenity

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'room_type', 'price_per_night', 'is_available']
    list_filter = ['room_type', 'is_available']

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ['name']