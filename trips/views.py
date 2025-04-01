from django.shortcuts import render, get_object_or_404, redirect  
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.dateparse import parse_datetime
from datetime import datetime
from django.http import JsonResponse

from auth_app.models import Driver
from trips.models import Trip  
from .forms import TripForm, TripUpdateForm, TripBookingForm

@login_required
def trip_list(request):
    user = request.user
    driver = Driver.objects.filter(user=user).first()  # Get the driver linked to the user

    # Fetch trips where the user is either a driver or a car owner
    trips_as_driver = Trip.objects.filter(driver=driver.user).order_by('-trip_date') if driver else Trip.objects.none()

    trips_as_owner = Trip.objects.filter(car_owner=user).order_by('-trip_date')

    if not trips_as_driver.exists() and not trips_as_owner.exists():
        messages.error(request, "You have no trips yet. Book a trip to get started!")

        if driver:  
            return redirect('hire_driver', driver_id=driver.id)  
        else:  
            return render(request, 'auth_app/driver_list.html')  # ✅ Redirects to driver_list.html

    return render(request, 'trips/trip_list.html', {
        'trips_as_driver': trips_as_driver,
        'trips_as_owner': trips_as_owner,
        'is_driver': driver is not None
    })

@login_required
def trip_create(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.driver = request.user.driver
            trip.save()
            messages.success(request, 'Trip created successfully!')
            return redirect('trip_list')
    else:
        form = TripForm()
    return render(request, 'trips/trip_create.html', {'form': form})

@login_required
def trip_update(request, trip_id):  
    trip = get_object_or_404(Trip, pk=trip_id)
    if request.method == 'POST':
        form = TripUpdateForm(request.POST, instance=trip)
        if form.is_valid():
            form.save()
            messages.success(request, 'Trip updated successfully!')
            return redirect('trip_list')
    else:
        form = TripUpdateForm(instance=trip)
    return render(request, 'trips/trip_update.html', {'form': form})

@login_required
def trip_detail(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)
    return render(request, 'trips/trip_detail.html', {'trip': trip})

@login_required
def trip_delete(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)
    trip.delete()
    messages.success(request, 'Trip deleted successfully!')
    return redirect('trip_list')

@login_required
def hire_driver(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)

    if request.method == "POST":
        departure_time = parse_datetime(request.POST.get('departure_time'))
        arrival_time = parse_datetime(request.POST.get('arrival_time'))
        pickup_point = request.POST.get('pickup_point')
        destination = request.POST.get('destination')
        payment_offered = request.POST.get('payment_offered')

        if not departure_time or not arrival_time:
            messages.error(request, "Please enter both departure and arrival times.")
            return render(request, 'auth_app/hire_driver.html', {'driver': driver})

        if arrival_time < departure_time:
            messages.error(request, "Arrival time must be after departure time.")
            return render(request, 'auth_app/hire_driver.html', {'driver': driver})

        if departure_time < datetime.now():
            messages.error(request, "Departure time must be in the future.")
            return render(request, 'auth_app/hire_driver.html', {'driver': driver})

        trip = Trip.objects.create(
            car_owner=request.user,
            driver=driver.user,
            destination=destination,
            pickup_location=pickup_point,
            trip_date=departure_time,
            price=payment_offered,
            status="pending"
        )
        messages.success(request, 'Trip created successfully!')
        return redirect('trip_list')

    return render(request, 'auth_app/hire_driver.html', {'driver': driver})
