from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('car_owner/register/', views.register_car_owner, name='register_car_owner'),
    path('car_owner/<int:owner_id>/', views.car_owner_details, name='car_owner_details'),
    path('trips/', views.trip_list, name='trip_list'),
    path('trips/<int:trip_id>/', views.trip_detail, name='trip_detail'),
    path('trips/<int:trip_id>/update/', views.trip_update, name='trip_update'),
    path('trips/<int:trip_id>/track/', views.track_trip, name='track_trip'),
    path('profile/', views.profile, name='profile'),
    path('become_driver/', views.become_driver, name='become_driver'),
    path('view_driver_application/', views.view_driver_application, name='view_driver_application'),
    path('update_driver_profile/<int:driver_id>/', views.update_driver_profile, name='update_driver_profile'),
    path('hire_driver/<int:driver_id>/', views.hire_driver, name='hire_driver'),
    path('api/register/', views.api_register, name='api_register'),
    path('api/login/', views.ApiLoginView.as_view(), name='api_login'),
    path('verify/<str:token>/', views.verify_email, name='verify_email'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/<str:token>/', views.reset_password, name='reset_password'),
    path('carowner/application/', views.view_carowner_application, name='view_carowner_application'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Your existing URLs...
]

# Only serve media files in development mode
