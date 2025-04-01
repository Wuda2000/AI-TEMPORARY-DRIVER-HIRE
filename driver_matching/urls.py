from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.index, name='driver_matching_index'),
    path('drivers/', views.driver_list, name='driver_list'),  # Added URL pattern for driver_list
]
