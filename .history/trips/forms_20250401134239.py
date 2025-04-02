from django import forms
from auth_app.models import Trip, CustomUser  

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['destination', 'pickup_location', 'trip_date']
        widgets = {
            'trip_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_trip_date(self):
        trip_date = self.cleaned_data.get('trip_date')
        if trip_date and trip_date < datetime.now():
            raise ValidationError("The trip date must be in the future.")
        return trip_date
class TripUpdateForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['destination', 'pickup_location', 'trip_date', 'status']
        widgets = {
            'trip_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }



class TripBookingForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['destination', 'pickup_location', 'trip_date', 'car_owner', 'driver']
        widgets = {
            'trip_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure the User model has a 'role' field
        self.fields['driver'].queryset = CustomUser.objects.filter(role='Driver')  # Ensure role matches stored values
        self.fields['car_owner'].queryset = CustomUser.objects.filter(role='CarOwner') 



class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser

        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'readonly': True}),
            'email': forms.EmailInput(attrs={'readonly': True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].disabled = True
        self.fields['email'].disabled = True
