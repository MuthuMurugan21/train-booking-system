from django.shortcuts import render, get_object_or_404, redirect
from .models import Train, SeatCategory, Passenger, Booking
from django.contrib.auth.decorators import login_required

def home(request):
    trains = Train.objects.all()
    return render(request, 'home.html', {'trains': trains})

@login_required
def book_ticket(request, train_id):
    train = get_object_or_404(Train, id=train_id)
    categories = SeatCategory.objects.filter(train=train)

    if request.method == 'POST':
        name = request.POST['name']
        age = request.POST['age']
        gender = request.POST['gender']
        category_id = request.POST['category']
        category = SeatCategory.objects.get(id=category_id)

        if category.available_seats > 0:
            passenger = Passenger.objects.create(name=name, age=age, gender=gender)
            Booking.objects.create(user=request.user, train=train, seat_category=category, passenger=passenger, status='Confirmed')
            category.available_seats -= 1
            category.save()
            return redirect('success')
        else:
            return render(request, 'book_ticket.html', {'train': train, 'categories': categories, 'error': 'No seats available!'})

    return render(request, 'book_ticket.html', {'train': train, 'categories': categories})

def success(request):
    return render(request, 'success.html')
