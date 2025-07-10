from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Train, SeatCategory, Passenger, Booking   # ✅ Add Booking!
from django.forms import formset_factory
from .forms import PassengerForm


def home(request):
    trains = Train.objects.all()

    source = request.GET.get('source')
    destination = request.GET.get('destination')

    if source and destination:
        trains = trains.filter(source__icontains=source, destination__icontains=destination)

    return render(request, 'home.html', {'trains': trains})

def success(request):
    return render(request, 'success.html')

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'my_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.status = 'Cancelled'
    booking.seat_category.available_seats += 1
    booking.seat_category.save()
    booking.save()
    return redirect('my_bookings')


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
            total_passengers = len(formset)
            if category.available_seats >= total_passengers:
                booking = Booking.objects.create(
                    user=request.user,
                    train=train,
                    seat_category=category,
                    travel_date=travel_date,
                    status='Confirmed'
                )
                for form in formset:
                    passenger = form.save(commit=False)
                    passenger.booking = booking
                    passenger.save()

                category.available_seats -= total_passengers
                category.save()
                return redirect('success')
            else:
                return render(request, 'book_ticket.html', {
                    'train': train, 'categories': categories, 'formset': formset,
                    'error': 'Not enough seats available!'
                })

    else:
        formset = PassengerFormSet()

    return render(request, 'book_ticket.html', {
        'train': train, 'categories': categories, 'formset': formset
    })

@login_required
def payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        booking.status = 'Paid'
        booking.save()
        return redirect('success')
    return render(request, 'payment.html', {'booking': booking})
