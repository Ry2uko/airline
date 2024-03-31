from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Flight, Airport, Passenger

def index(request):
    return render(request, 'flights/index.html', {
        'flights': Flight.objects.all(),
    })


def flight(request, flight_id):
    flight = Flight.objects.get(id=flight_id)
    passengers = flight.passengers.all()
    non_passengers = Passenger.objects.exclude(flights=flight).all() if request.user.is_authenticated else []
    
    return render(request, 'flights/flight.html', {
        'flight': flight,
        'passengers': passengers,
        'non_passengers': non_passengers,
        'user_is_authenticated': request.user.is_authenticated
    })


def book(request, flight_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('flights:flight', args=(flight_id,)))
    
    if request.method == 'POST':
        flight = Flight.objects.get(id=flight_id)
        passenger_id = int(request.POST['passenger'])

        passenger = Passenger.objects.get(pk=passenger_id)
        passenger.flights.add(flight)

        return HttpResponseRedirect(reverse('flights:flight', args=(flight_id,)))