import uuid
from django import forms
from django.contrib.auth.forms import UserCreationForm
from auth_app.models import CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from auth_app.models import CustomUser  
from .models import DriverApplication, Driver, Trip, CarOwner, Car
from django.core.exceptions import ValidationError
from django.forms.widgets import ClearableFileInput       
from django import forms
from auth_app.models import CarOwner

class CarOwnerForm(forms.ModelForm):
    # Customizing the year field to make its purpose clearer
    year = forms.IntegerField(
        label="Year of Registration",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter year of registration'}),
        help_text="Enter the year you registered as a car owner."
    )

    # Optionally adding a profile image field back
    profile_image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        help_text="Upload a profile picture (optional)."
    )

    class Meta:
        model = CarOwner
        fields = ['name', 'year', 'phone_number', 'email', 'profile_image']  # Included 'profile_image' again

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adding custom attributes for styling, if needed
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your name'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your phone number'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your email'})

from django import forms
from auth_app.models import CarOwner
from django.core.exceptions import ValidationError
import re  # To use for password strength check

class CarOwnerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = CarOwner
        fields = ['name', 'year', 'phone_number', 'email']  # Personal details only

    def clean(self):
        cleaned_data = super().clean()

        # Password confirmation validation
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")
        
        # Custom password strength validation
        self.validate_password_strength(password)

        return cleaned_data

    def validate_password_strength(self, password):
        """
        This method checks if the password meets the required strength criteria:
        - At least 8 characters long
        - Contains at least one digit
        - Contains at least one letter
        - Contains at least one special character
        - Contains at least one uppercase letter
        """
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        
        if not any(char.isdigit() for char in password):
            raise ValidationError("Password must contain at least one digit.")
        
        if not any(char.isalpha() for char in password):
            raise ValidationError("Password must contain at least one letter.")
        
        if not any(char.isupper() for char in password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        
        if not any(char in "!@#$%^&*()-_+=<>?" for char in password):
            raise ValidationError("Password must contain at least one special character (e.g., !@#$%^&*).")
        
        return password
from django import forms
from auth_app.models import Car
from django.core.exceptions import ValidationError

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['make', 'model', 'plate_number', 'capacity', 'car_type', 'car_color', 'car_image']
    
    def clean_car_image(self):
        car_image = self.cleaned_data.get('car_image')
        
        # Check if image size is less than 5MB
        if car_image:
            max_size = 5 * 1024 * 1024  # 5MB in bytes
            if car_image.size > max_size:
                raise ValidationError("The image size must be less than 5MB.")
            
            # Check if image format is one of the allowed types
            allowed_extensions = ['jpg', 'jpeg', 'png']
            file_extension = car_image.name.split('.')[-1].lower()
            if file_extension not in allowed_extensions:
                raise ValidationError("Only .jpg, .jpeg, and .png formats are allowed.")
        
        return car_image

class CarDetailsForm(forms.ModelForm):
    car_image = forms.ImageField(required=True)
    class Meta:
        model = Car
        fields = ['car_type', 'car_color', 'plate_number', 'capacity', 'car_image']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'user_type')

    def clean_email(self):
        """Validate email uniqueness at the form level."""
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered. Please use a different one.")
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("Password must contain at least one digit.")
        if not any(char.isalpha() for char in password):
            raise forms.ValidationError("Password must contain at least one letter.")
        return password


class DriverApplicationForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    surname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    age = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 21}))

    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        age = cleaned_data.get('age')
        if age and age < 21:
            self.add_error('age', "You must be at least 21 years old to apply.")
            
    ethnicity = forms.ChoiceField(
        choices=[('Kikuyu', 'Kikuyu'), ('Luo', 'Luo'), ('Luhya', 'Luhya'), ('Kalenjin', 'Kalenjin'), ('Kamba', 'Kamba'), ('Other', 'Other')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    kcse_certificate = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    good_conduct = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    cover_letter = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    cv = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    experience_years = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0}), required=True)
    
    class Meta:
        model = DriverApplication
        fields = ['first_name', 'surname', 'age' ,'ethnicity', 'experience_years',
                  'kcse_certificate', 'good_conduct', 'cover_letter', 'cv', 'email']

    def clean_email(self):
        """Validate email uniqueness at the form level.""" 
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered. Please use a different one.")
        return email

    def save(self, commit=True):
        application = super().save(commit=False)
        if commit:
            application.save()
        return application

class DriverProfileForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['name', 'license_number', 'experience_years', 'profile_picture']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'}),
            'license_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter license number'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Years of experience'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class DriverProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['experience_years', 'rating', 'price_per_trip', 'location', 'phone_number', 'bio', 'profile_picture']

    profile_picture = forms.FileField(
        widget=forms.ClearableFileInput(),
        required=False
    )

    additional_images = forms.FileField(
        widget=forms.ClearableFileInput(),
        required=False
    )

    def clean_additional_images(self):
        files = self.files.getlist('additional_images')

        if len(files) > 3:
            raise ValidationError("You can only upload up to 3 additional images.")
        return files
    
class HireDriverForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['departure_time', 'arrival_time', 'pickup_point', 'destination', 'trip_distance', 'payment_offered']
        widgets = {
            'departure_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'arrival_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class TripUpdateForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ["status"]
