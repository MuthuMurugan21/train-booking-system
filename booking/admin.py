from django.contrib import admin
from .models import Train, SeatCategory, Passenger, Booking

admin.site.register(Train)
admin.site.register(SeatCategory)
admin.site.register(Passenger)
admin.site.register(Booking)
