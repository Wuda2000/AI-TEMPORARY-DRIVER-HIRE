from django.shortcuts import render
from django.http import HttpResponse
from .models import DriverMatch  # Importing the DriverMatch model
from auth_app.models import Driver

def index(request):
    return HttpResponse("Driver Matching App is working!")

def driver_list(request):
    drivers = Driver.objects.all()  # Retrieve all drivers from the database
    return render(request, 'auth_app/driver_list.html', {'drivers': drivers})
