from django.contrib import admin
from .models import DriverMatch  # Import necessary models

@admin.register(DriverMatch)
class DriverMatchAdmin(admin.ModelAdmin):
    list_display = ("id", "driver", "car_owner", "trip_date", "match_score")  # Display key fields
    search_fields = ("driver__username", "car_owner__username")  # Enable search by related user fields
    list_filter = ("trip_date", "match_score")  # Filter by trip date and match score
    ordering = ("-trip_date",)  # Order by most recent trips

    actions = ["approve_match", "reject_match"]  # Define custom admin actions

    def approve_match(self, request, queryset):
        queryset.update(status="Approved")
        self.message_user(request, "Selected matches have been approved.")
    approve_match.short_description = "Approve selected matches"

    def reject_match(self, request, queryset):
        queryset.update(status="Rejected")
        self.message_user(request, "Selected matches have been rejected.")
    reject_match.short_description = "Reject selected matches"

# Removed registration for AnotherModel as it does not exist
