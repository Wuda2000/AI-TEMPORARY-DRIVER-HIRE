import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from auth_app.models import CustomUser
from django.shortcuts import render, get_object_or_404, redirect
from .models import CarOwner, Car
from .forms import CarOwnerForm, CarForm
from django.http import JsonResponse, HttpResponseForbidden
from django.core.mail import send_mail
from django.utils.crypto import get_random_string  
from django.urls import reverse  
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError, PermissionDenied
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.contrib.auth.password_validation import validate_password
from rest_framework.views import APIView  
from django.contrib.auth.models import User, Group
from .forms import (
    CustomUserCreationForm, DriverApplicationForm, HireDriverForm, 
    DriverProfileUpdateForm, DriverProfileForm, TripUpdateForm, CarOwnerForm, CarForm, CarOwnerRegistrationForm, CarDetailsForm
)
from .models import (
    CustomUser, DriverApplication, Driver, CarOwner, Trip, DriverApplicationContent, CarOwner, Car
)
from reviews.models import Review

from .utils import send_verification_email
from django.conf import settings
from auth_app.forms import CarOwnerRegistrationForm, CarOwnerForm




OPENROUTE_API_KEY = settings.OPENROUTE_API_KEY



@ensure_csrf_cookie
def home(request):
    return render(request, 'auth_app/home.html')

@ensure_csrf_cookie
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'auth_app/login.html')

@login_required
@ensure_csrf_cookie
def dashboard(request):
    trip_list_url = reverse('trip_list')
    is_driver = getattr(request.user, "role", None) == "driver"
    driver = Driver.objects.filter(user=request.user).first()

    context = {
        'is_driver': is_driver,
        'user': request.user,
        'trip_list_url': trip_list_url,
        'driver': driver,
    }
    return render(request, 'auth_app/dashboard.html', context)


def register_car_owner(request):
    if request.method == 'POST':
        owner_form = CarOwnerForm(request.POST)
        car_form = CarForm(request.POST, request.FILES)
        if owner_form.is_valid() and car_form.is_valid():
            owner = owner_form.save()
            car = car_form.save(commit=False)
            car.owner = owner
            car.save()
            return redirect('view_carowner_application', owner_id=owner.id)
    else:
        owner_form = CarOwnerForm()
        car_form = CarForm()
    
    return render(request, 'auth_app/carowner/register_car_owner.html', {
        'owner_form': owner_form,
        'car_form': car_form,
    })

def view_carowner_application(request):
    return render(request, 'auth_app/carowner/view_carowner_application.html')


def car_owner_details(request, owner_id):
    car_owner = get_object_or_404(CarOwner, id=owner_id)
    return render(request, 'auth_app/carowner/car_owner_details.html', {'car_owner': car_owner, 'car': car_owner.car})


@login_required
@ensure_csrf_cookie
def trip_list(request):
    user = request.user
    driver = Driver.objects.filter(user=user).first()  
    trips_as_driver = Trip.objects.filter(driver=driver.user).order_by('-created_at') if driver else Trip.objects.none()

    pending_trips = Trip.objects.filter(status="Pending")

    return render(request, "trip_list.html", {
        "pending_trips": pending_trips,
        "trips_as_driver": trips_as_driver
    })

@ensure_csrf_cookie
def trip_detail(request, id):
    trip = get_object_or_404(Trip, id=id)
    return render(request, "trip_detail.html", {"trip": trip})

@ensure_csrf_cookie
def trip_update(request, id):
    trip = get_object_or_404(Trip, id=id)
    
    if request.method == "POST":
        form = TripUpdateForm(request.POST, instance=trip)
        if form.is_valid():
            form.save()
            return redirect("trip_list")
    else:
        form = TripUpdateForm(instance=trip)

    return render(request, "trip_update.html", {"form": form, "trip": trip})

@ensure_csrf_cookie
def track_trip(request, id):
    trip = get_object_or_404(Trip, id=id)
    return render(request, "real_time_tracking.html", {"trip": trip})

@login_required
@ensure_csrf_cookie
def profile(request):
    role = getattr(request.user, "role", None)
    driver = Driver.objects.filter(user=request.user).first() if role == "driver" else None
    car_owner = CarOwner.objects.filter(user=request.user).first() if role == "carOwner" else None

    return render(request, 'auth_app/profile.html', {
        'user': request.user,
        'driver': driver,
        'car_owner': car_owner
    })

@login_required
@ensure_csrf_cookie
def become_driver(request):
    if DriverApplication.objects.filter(user=request.user).exists():
        messages.warning(request, "You have already applied to become a driver.")
        return redirect('dashboard')

    if request.method == "POST":
        try:
            age = int(request.POST.get("age", 0))
            experience_years = int(request.POST.get("experience_years", 0))


        except ValueError:
            messages.error(request, "Invalid age or experience value.")
            return redirect('become_driver')

        if age < 21:
            messages.error(request, "You must be at least 21 years old to apply.")
            return redirect('become_driver')

        if experience_years < 1:

            messages.error(request, "You must have at least 1 year of driving experience.")
            return redirect('become_driver')

        DriverApplication.objects.create(
            user=request.user,
            first_name=request.POST.get("first_name"),
            surname=request.POST.get("surname"),
            age=age,
            experience_years=experience_years,

            kcse_certificate=request.FILES.get("kcse_certificate"),
            good_conduct=request.FILES.get("good_conduct"),
            cover_letter=request.FILES.get("cover_letter"),
            license_number=request.POST.get("license_number"),  

            cv=request.FILES.get("cv")
        )

        messages.success(request, "Application submitted successfully. Please wait for approval.")
        return redirect('dashboard')

    return render(request, "auth_app/become_driver.html")

def become_driver_view(request):  
    content = DriverApplicationContent.objects.first()  
    if not content:  
        content = "<p>No content available. Please add it through the admin.</p>"  

    return render(request, "auth_app/become_driver.html", {  
        'content': content.content,  
    })  

@login_required
def update_driver_application_content(request):
    if not request.user.is_superuser:
        raise PermissionDenied("Access Denied: Only Admins Can Edit This Content.")

    if request.method == "POST":
        content = request.POST.get("content", "")
        DriverApplicationContent.objects.update_or_create(defaults={"content": content})
        return JsonResponse({"message": "Content updated successfully."})

    return JsonResponse({"error": "Invalid request."}, status=400)

@login_required
@ensure_csrf_cookie
def view_driver_application(request):
    if getattr(request.user, "role", None) != "driver":
        return HttpResponseForbidden("You are not authorized to view this page.")

    application = DriverApplication.objects.filter(user=request.user).first()

    if application is None:
        messages.error(request, "No application found. Please submit your application first.")
        return redirect('become_driver')  # Redirect to the application form or another appropriate page


    return render(request, "auth_app/view_driver_application.html", {
        "application": application,
        "cover_letter": bool(application.cover_letter),
        "cv": bool(application.cv),
        "kcse_certificate": bool(application.kcse_certificate),
        "driver_license": bool(application.license_number),

        "good_conduct": bool(application.good_conduct),
    })

@login_required
def update_driver_profile(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)  

    if driver.user != request.user:
        print("Unauthorized access attempt.")
        return redirect('dashboard')  

    if request.method == "POST":
        form = DriverProfileForm(request.POST, request.FILES, instance=driver)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  
    else:
        form = DriverProfileForm(instance=driver)

    return render(request, 'auth_app/update_driver_profile.html', {'form': form})


@login_required
def hire_driver(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    car_owner = get_object_or_404(CarOwner, user=request.user)

    if request.method == 'POST':
        form = HireDriverForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.driver = driver
            trip.car_owner = car_owner
            trip.status = "Pending"
            trip.save()
            request.session['id'] = trip.id  # Store trip ID for payment processing
            return redirect('process_payment', trip.id)  # Redirect to payment

    else:
        form = HireDriverForm()

    return render(request, 'auth_app/hire_driver.html', {'form': form, 'driver': driver})

def get_api_key(request):
    """ Securely fetch API key """
    return JsonResponse({'api_key': OPENROUTE_API_KEY})


def verify_email(request, token):
    try:
        user = CustomUser.objects.get(email_verification_token=token)
        if user.verification_token_created_at < timezone.now() - timedelta(days=1):
            return JsonResponse({'error': 'Verification link expired.'}, status=400)

        user.is_active = True
        user.email_verification_token = None
        user.save()
        return JsonResponse({'message': 'Email verified successfully.'})
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'Invalid token.'}, status=400)

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.filter(email=email).first()  

            if not user:
                return JsonResponse({'error': 'Email not found.'}, status=400)

            reset_token = get_random_string(length=32)
            user.password_reset_token = reset_token
            user.save()

            reset_link = request.build_absolute_uri(reverse('reset_password', args=[reset_token]))
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_link}',
                'noreply@autotempohire.com',
                [email],
                fail_silently=False,
            )
            return JsonResponse({'message': 'Password reset link sent to your email.'}, status=200)

        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)

    return render(request, 'auth_app/forgot_password.html')

def reset_password(request, token):
    if request.method == 'POST':
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            return JsonResponse({'error': 'Passwords do not match.'}, status=400)

        try:
            validate_password(new_password)  
        except ValidationError as e:
            return JsonResponse({'error': e.messages}, status=400)

        try:
            user = CustomUser.objects.get(password_reset_token=token)
            user.set_password(new_password)
            user.password_reset_token = None  
            user.save()
            return JsonResponse({'message': 'Password reset successful. Please login with your new password.'}, status=200)

        except ValidationError as e:
            return JsonResponse({'error': e.messages}, status=400)  

        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'Invalid token.'}, status=400)

    return render(request, 'auth_app/reset_password.html', {'token': token})

def api_register(request):
    print("API Register called")  # Debugging line
    print("Request method:", request.method)  # Debugging line
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password1')
        confirm_password = data.get('password2')
        role = data.get('role')

        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({'error': 'This email is already registered. Please use a different one.'}, status=400)

        if CustomUser.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists.'}, status=400)

        if password != confirm_password:
            return JsonResponse({'error': 'Passwords do not match.'}, status=400)

        try:
            validate_password(password)  

            user = CustomUser.objects.create_user(
                username=username, 
                email=email, 
                password=password,
                role=role
            )

            group = Group.objects.get_or_create(name='CarOwners' if role == 'carOwner' else 'Drivers')[0]
            user.groups.add(group)

            return JsonResponse({'message': 'User registered successfully.'}, status=201)

        except ValidationError as e:
            return JsonResponse({'error': e.messages}, status=400)  

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

class ApiLoginView(APIView):
    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful.'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid credentials.'}, status=401)
def send_verification_email(user):  
    """Send an email verification link after user registration."""  
    verification_token = get_random_string(length=32)
    user.email_verification_token = verification_token  
    user.verification_token_created_at = timezone.now()  
    user.save()

    verification_link = f"http://127.0.0.1:8000/auth/verify/{verification_token}/"

    send_mail(
        'Verify Your Email - AutoTempoHire',
        f'Hello {user.username},\n\nClick the link below to verify your email:\n{verification_link}',
        'fridawawuda@gmail.com',  
        [user.email],
        fail_silently=False,
    )


def register(request):  
    """Handle user registration and send verification email."""  
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Fix commit=False usage
            user.is_active = False  # Mark as inactive until verified
            user.save()

            send_verification_email(user)

            return redirect('registration_success')  # Redirect to success page
    else:
        form = CustomUserCreationForm()

    return render(request, 'auth_app/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')
