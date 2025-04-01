from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import csv
import pdfkit
from django.template.loader import render_to_string  # Added missing import
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Payment

@login_required
def payment_history_view(request):
    """
    Fetch and display payment history for the logged-in user.
    Includes pagination to improve performance.
    """
    # Fetch payments for the logged-in user (optimized query)
    payments = Payment.objects.filter(user=request.user).order_by('-date').only('amount', 'status', 'date', 'id')

    # Paginate results (10 payments per page)
    paginator = Paginator(payments, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Check user role and filter payments accordingly
    user_role = request.user.role  # Assuming user role is stored in a 'role' attribute
    if user_role == 'Car Owner':
        payments = payments.filter(car_owner=request.user)
    elif user_role == 'Driver':
        payments = payments.filter(driver=request.user)
    elif user_role == 'Admin':
        payments = payments  # Admin can see all payments

    # Export functionality
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="payment_history.csv"'
        writer = csv.writer(response)
        writer.writerow(['Date', 'Amount', 'Status'])
        for payment in payments:
            writer.writerow([payment.date, payment.amount, payment.status])
        return response

    elif request.GET.get('export') == 'pdf':
        html = render_to_string("payments/payment_history.html", {"page_obj": page_obj})
        pdf = pdfkit.from_string(html, False)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="payment_history.pdf"'
        return response

    return render(request, "payments/payment_history.html", {
        "payments": payments,  # Pass the payments to the template
        "page_obj": page_obj  # Pass paginated payments
    })