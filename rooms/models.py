from django.db import models

class Amenity(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, default='fa-check')

    def __str__(self):
        return self.name

class Room(models.Model):
    ROOM_TYPES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite', 'Suite'),
        ('deluxe', 'Deluxe'),
        ('presidential', 'Presidential'),
    ]
    name = models.CharField(max_length=100)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField(default=2)
    size_sqm = models.IntegerField(default=25)
    description = models.TextField()
    image = models.ImageField(upload_to='rooms/')
    images = models.JSONField(default=list, blank=True)  # multiple images
    amenities = models.ManyToManyField(Amenity, blank=True)
    is_available = models.BooleanField(default=True)
    total_rooms = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.room_type}"

    @property
    def available_count(self):
        from bookings.models import Booking
        from django.utils import timezone
        active = Booking.objects.filter(
            room=self,
            status__in=['confirmed', 'checked_in'],
            check_out__gt=timezone.now().date()
        ).count()
        return max(0, self.total_rooms - active)