from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/<int:train_id>/', views.book_ticket, name='book_ticket'),
    path('success/', views.success, name='success'),
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('buses/', views.bus_home, name='bus_home'),
    path('book_bus/<int:bus_id>/', views.book_bus_ticket, name='book_bus_ticket'),
    path('my_bus_bookings/', views.my_bus_bookings, name='my_bus_bookings'),
    path('cancel_bus/<int:booking_id>/', views.cancel_bus_booking, name='cancel_bus_booking'),
]
