
from django.db import models
from django.contrib.auth.models import User

# 1️⃣ Train table
class Train(models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=10)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()

    def __str__(self):
        return f"{self.number} - {self.name}"

# 2️⃣ SeatCategory table
class SeatCategory(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=50)
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()

    def __str__(self):
        return f"{self.train.name} - {self.category_name}"

# 3️⃣ Booking table
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    seat_category = models.ForeignKey(SeatCategory, on_delete=models.CASCADE)
    travel_date = models.DateField(null=True)
    booking_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"Booking #{self.id}"

# 4️⃣ Passenger table
class Passenger(models.Model):
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE, related_name='passengers')
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.name
