from django.contrib.auth.models import Group 
from django.db.utils import OperationalError, ProgrammingError
from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from .models import CustomUser, DriverApplication  # Importing the actual models

# Ensure 'CarOwners' and 'Drivers' groups exist after migrations
@receiver(post_migrate)
def create_groups(sender, **kwargs):
    try:
        for group_name in ["CarOwners", "Drivers"]:
            Group.objects.get_or_create(name=group_name)
    except (OperationalError, ProgrammingError):
        # Ignore errors if the database is not fully ready
        pass

# Signal for post_save on CustomUser
@receiver(post_save, sender=CustomUser)
def create_user_groups(sender, instance, created, **kwargs):
    if created:
        # Automatically assign the user to default groups
        if instance.role == 'carOwner':
            instance.groups.add(Group.objects.get(name='CarOwners'))
        elif instance.role == 'driver':
            instance.groups.add(Group.objects.get(name='Drivers'))

# Signal for post_save on DriverApplication
@receiver(post_save, sender=DriverApplication)
def notify_driver_application(sender, instance, created, **kwargs):
    if created:
        # Perform actions when a new driver application is created
        pass
