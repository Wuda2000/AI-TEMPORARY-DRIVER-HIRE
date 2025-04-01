import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Payment

@pytest.mark.django_db
def test_payment_history_no_payments(client):
    user = User.objects.create_user(username='user', password='testpass')
    client.login(username='user', password='testpass')

    response = client.get(reverse('payment_history_view'))
    assert response.status_code == 200
    assert 'No payments found' in response.content.decode()  # Check for no payments message

@pytest.mark.django_db
def test_payment_history_filtering(client):
    # Create users with different roles
    car_owner = User.objects.create_user(username='car_owner', password='testpass')
    driver = User.objects.create_user(username='driver', password='testpass')
    admin = User.objects.create_user(username='admin', password='testpass')

    # Create payment records
    Payment.objects.create(user=car_owner, amount=100, status='Completed')
    Payment.objects.create(user=driver, amount=200, status='Pending')

    # Log in as car owner and check payment history
    client.login(username='car_owner', password='testpass')
    response = client.get(reverse('payment_history_view'))
    assert response.status_code == 200
    assert '100' in response.content.decode()  # Check if car owner's payment is present
    assert '200' not in response.content.decode()  # Check if driver's payment is not present

    # Log in as driver and check payment history
    client.login(username='driver', password='testpass')
    response = client.get(reverse('payment_history_view'))
    assert response.status_code == 200
    assert '200' in response.content.decode()  # Check if driver's payment is present
    assert '100' not in response.content.decode()  # Check if car owner's payment is not present

@pytest.mark.django_db
def test_payment_history_pagination(client):
    user = User.objects.create_user(username='user', password='testpass')
    client.login(username='user', password='testpass')

    # Create 15 payment records
    for i in range(15):
        Payment.objects.create(user=user, amount=i * 10, status='Completed')

    response = client.get(reverse('payment_history_view') + '?page=1')
    assert response.status_code == 200
    assert len(response.context['page_obj']) == 10  # Check if first page has 10 payments

    response = client.get(reverse('payment_history_view') + '?page=2')
    assert response.status_code == 200
    assert len(response.context['page_obj']) == 5  # Check if second page has remaining 5 payments

@pytest.mark.django_db
def test_payment_history_export_csv(client):
    user = User.objects.create_user(username='user', password='testpass')
    client.login(username='user', password='testpass')

    Payment.objects.create(user=user, amount=100, status='Completed')
    response = client.get(reverse('payment_history_view') + '?export=csv')
    assert response.status_code == 200
    assert response['Content-Type'] == 'text/csv'
    assert 'Date,Amount,Status' in response.content.decode()  # Check CSV header

@pytest.mark.django_db
def test_payment_history_invalid_filters(client):
    user = User.objects.create_user(username='user', password='testpass')
    client.login(username='user', password='testpass')

    response = client.get(reverse('payment_history_view') + '?invalid_param=value')
    assert response.status_code == 200  # Check if the view handles invalid filters gracefully
    assert 'Invalid filter' in response.content.decode()  # Check for invalid filter message

@pytest.mark.django_db
def test_payment_history_export_pdf(client):
    user = User.objects.create_user(username='user', password='testpass')
    client.login(username='user', password='testpass')

    Payment.objects.create(user=user, amount=100, status='Completed')
    response = client.get(reverse('payment_history_view') + '?export=pdf')
    assert response.status_code == 200
    assert response['Content-Type'] == 'application/pdf'

@pytest.mark.django_db
def test_payment_history_unauthorized_access(client):
    response = client.get(reverse('payment_history_view'))
    assert response.status_code == 302  # Check for redirect to login page
    assert 'Login' in response.content.decode()  # Check for login prompt
