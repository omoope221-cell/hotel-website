# bookings/admin.py
from django.contrib import admin
from .models import Booking, ContactMessage

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['guest_name', 'room', 'check_in', 'check_out', 'status']
    list_filter = ['status', 'check_in']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']