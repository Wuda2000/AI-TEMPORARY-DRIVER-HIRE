from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.core.mail import send_mail
from auth_app.models import (
    CustomUser, Car, CarOwner, Trip, DriverApplication, Driver, 
    DriverApplicationContent
)
from reviews.models import Review

# Registering models
admin.site.register(Review)

# Prevent duplicate registration
if admin.site.is_registered(DriverApplication):
    admin.site.unregister(DriverApplication)

@admin.register(CarOwner)
class CarOwnerAdmin(admin.ModelAdmin):
    list_display = ("name", "email",  "status")  # Added status field
    list_filter = ("status",)  # Added status field for filtering
    search_fields = ('name', 'phone_number', 'email')

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'plate_number', 'capacity', 'car_type', 'owner')
    search_fields = ('make', 'model', 'plate_number')

@admin.register(DriverApplication)
class DriverApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'surname', 'age', 'license_number', 'experience_years', 'status', 'applied_at')
    list_filter = ('status', 'experience_years')
    search_fields = ('user__username', 'first_name', 'surname', 'license_number')
    actions = ['approve_application', 'reject_application']

    def approve_application(self, request, queryset):
        queryset.update(status='Approved')
        emails = list(queryset.values_list('user__email', flat=True))
        send_mail(
            "Driver Application Approved",
            "Your driver application has been approved!",
            "admin@autotempohire.com",
            emails,
            fail_silently=False,
        )
        self.message_user(request, "Selected applications have been approved.")
    approve_application.short_description = "Approve selected applications"

    def reject_application(self, request, queryset):
        queryset.update(status='Rejected')
        emails = list(queryset.values_list('user__email', flat=True))
        send_mail(
            "Driver Application Rejected",
            "Your driver application has been rejected. Please contact support.",
            "admin@autotempohire.com",
            emails,
            fail_silently=False,
        )
        self.message_user(request, "Selected applications have been rejected.")
    reject_application.short_description = "Reject selected applications"

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'license_number', 'experience_years', 'user')
    list_filter = ('experience_years',)

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'unique_id', 'is_verified', 'is_staff', 'password_last_changed_display', 'password_reset_token')
    search_fields = ('username', 'email', 'unique_id','password_last_changed', 'password_reset_token')
    list_filter = ('role', 'is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),  
        ('Personal Info', {'fields': ('unique_id', 'role', 'password_reset_token')}),  
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),  
        ('Important Dates', {'fields': ('last_login', 'date_joined', 'password_last_changed')}),  
    )

    readonly_fields = ('unique_id', 'password_last_changed', 'password_reset_token')

    def password_last_changed_display(self, obj):
        return obj.password_last_changed.strftime("%Y-%m-%d %H:%M:%S") if obj.password_last_changed else "Never Changed"
    password_last_changed_display.short_description = "Password Last Changed"

    def is_verified(self, obj):
        return format_html('<span style="color:{}; font-weight:bold;">{}</span>',
                           'green' if obj.is_active else 'red',
                           '✔️' if obj.is_active else '❌')
    is_verified.short_description = "Verified"

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ("destination", "status", "car_owner", "driver", "created_at", 'pickup_location', 'trip_date', 'trip_duration', 'amount', 'payment_offered', 'departure_time', 'arrival_time', 'trip_distance', 'pickup_point')
    list_filter = ("status",)
    search_fields = ("destination", "car_owner__username", "driver__username")

@admin.register(DriverApplicationContent)
class DriverApplicationContentAdmin(admin.ModelAdmin):
    list_display = ("id", "content_preview")
    search_fields = ("content",)

    def content_preview(self, obj):
        return obj.content[:100] + "..." if len(obj.content) > 100 else obj.content
    content_preview.short_description = "Content Preview"
