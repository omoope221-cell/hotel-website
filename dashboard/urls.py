from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('bookings/', views.bookings_list, name='bookings'),
    path('bookings/<int:pk>/', views.booking_update, name='booking_update'),
    path('bookings/<int:pk>/delete/', views.booking_delete, name='booking_delete'),
    path('rooms/', views.rooms_manage, name='rooms'),
    path('rooms/add/', views.room_add, name='room_add'),
    path('rooms/<int:pk>/edit/', views.room_edit, name='room_edit'),
    path('rooms/<int:pk>/delete/', views.room_delete, name='room_delete'),
    path('messages/', views.messages_list, name='messages'),
    path('messages/<int:pk>/', views.message_read, name='message_read'),
]
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('login/', views.dashboard_login, name='login'),
    path('logout/', views.dashboard_logout, name='logout'),
    path('', views.dashboard_home, name='home'),
    path('bookings/', views.bookings_list, name='bookings'),
    path('bookings/<int:pk>/', views.booking_update, name='booking_update'),
    path('bookings/<int:pk>/delete/', views.booking_delete, name='booking_delete'),
    path('rooms/', views.rooms_manage, name='rooms'),
    path('rooms/add/', views.room_add, name='room_add'),
    path('rooms/<int:pk>/edit/', views.room_edit, name='room_edit'),
    path('rooms/<int:pk>/delete/', views.room_delete, name='room_delete'),
    path('messages/', views.messages_list, name='messages'),
    path('messages/<int:pk>/', views.message_read, name='message_read'),
]