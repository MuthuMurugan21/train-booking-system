from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Train, SeatCategory, Booking, Passenger
from django.forms import formset_factory
from .forms import PassengerForm
from django.core.mail import send_mail
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse

@login_required
def download_ticket(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    template = get_template('ticket_pdf.html')
    html = template.render({'booking': booking})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{booking.id}.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response

def home(request):
    trains = Train.objects.all()
    source = request.GET.get('source')
    destination = request.GET.get('destination')

    if source:
        trains = trains.filter(source__icontains=source)
    if destination:
        trains = trains.filter(destination__icontains=destination)

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
    if booking.status == 'Confirmed' or booking.status == 'Paid':
        # ✅ use passenger_set if related_name not set
        booking.status = 'Cancelled'
        passenger_count = booking.passengers.count()  # OR booking.passenger_set.count()
        booking.seat_category.available_seats += passenger_count
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

                send_mail(
                    'Your Train Ticket Booking',
                    f'Thank you {request.user.username}! Your booking #{booking.id} is confirmed.',
                    'noreply@trainbooking.com',
                    [request.user.email],
                    fail_silently=True,
                )

                return redirect('payment', booking_id=booking.id)
            
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

@login_required
def ticket_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'ticket.html', {'booking': booking})
