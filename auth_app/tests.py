from django.test import TestCase
from .models import DriverApplication

class DriverApplicationTests(TestCase):
    def setUp(self):
        self.driver_application = DriverApplication.objects.create(
            first_name='John',
            surname='Doe',
            age=30,
            experience_years=2,
            license_number='ABC123',
            status='pending'
        )

    def test_driver_application_creation(self):
        self.assertEqual(self.driver_application.first_name, 'John')
        self.assertEqual(self.driver_application.surname, 'Doe')
        self.assertEqual(self.driver_application.age, 30)
        self.assertEqual(self.driver_application.experience_years, 2)  
        self.assertEqual(self.driver_application.license_number, 'ABC123')
        self.assertEqual(self.driver_application.status, 'pending')

    def test_driver_application_str(self):
        self.assertEqual(str(self.driver_application), 'John Doe - pending')

# Add more tests as necessary
