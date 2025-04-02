from django.urls import path
from .views import (
    trip_list,
    trip_create,
    trip_detail,
    trip_update,
    trip_delete,
    hire_driver
)

urlpatterns = [
    path('', trip_list, name='trip_list'),
    path('create/', trip_create, name='trip_create'),
    path('<int:id>/', trip_detail, name='trip_detail'),
    path('<int:id>/update/', trip_update, name='trip_update'),
    path('<int:id>/delete/', trip_delete, name='trip_delete'),
    path('hire/<int:driver_id>/', hire_driver, name='hire_driver'),  # Added hire driver route
]
