from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Train, SeatCategory, Booking, Passenger
from .forms import PassengerForm
from django.forms import formset_factory

def home(request):
    trains = Train.objects.all()
    return render(request, 'home.html', {'trains': trains})

@login_required
def book_ticket(request, train_id):
    train = get_object_or_404(Train, id=train_id)
    categories = SeatCategory.objects.filter(train=train)

    PassengerFormSet = formset_factory(PassengerForm, extra=1)

    if request.method == 'POST':
        travel_date = request.POST['travel_date']
        category_id = request.POST['category']
        category = SeatCategory.objects.get(id=category_id)

        formset = PassengerFormSet(request.POST)

        if formset.is_valid():
            booking = Booking.objects.create(
                user=request.user,
                train=train,
                seat_category=category,
                travel_date=travel_date,
                status='Confirmed'
            )

            for form in formset:
                Passenger.objects.create(
                    booking=booking,
                    name=form.cleaned_data['name'],
                    age=form.cleaned_data['age'],
                    gender=form.cleaned_data['gender']
                )

            # Update available seats
            category.available_seats -= len(formset)
            category.save()

            return redirect('success')

    else:
        formset = PassengerFormSet()

    return render(request, 'book_ticket.html', {
        'train': train,
        'categories': categories,
        'formset': formset
    })

@login_required
def success(request):
    return render(request, 'success.html')

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'my_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if booking.status == 'Confirmed':
        booking.status = 'Cancelled'
        booking.seat_category.available_seats += booking.passengers.count()
        booking.seat_category.save()
        booking.save()
    return redirect('my_bookings')
