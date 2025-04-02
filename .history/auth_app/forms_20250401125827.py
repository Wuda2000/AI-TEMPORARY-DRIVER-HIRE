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

class CarOwnerForm(forms.ModelForm):
    class Meta:
        model = CarOwner
        fields = ['name', 'year', 'phone_number', 'email']  # Removed 'model' and 'profile_image'

class CarOwnerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CarOwner
        fields = ['name', 'year', 'phone_number', 'email']  # Removed 'model' and 'profile_image'

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("confirm_password"):
            self.add_error('confirm_password', "Passwords do not match")
        return cleaned_data

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['make', 'model', 'plate_number', 'capacity', 'car_type', 'car_color', 'car_image']
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
