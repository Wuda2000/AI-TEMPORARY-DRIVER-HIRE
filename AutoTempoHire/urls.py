from django.contrib import admin 
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from tracking.urls import urlpatterns as tracking_urls  
from auth_app import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path('auth/', include('auth_app.urls')),  
    path('', views.home, name='home'),
    path('driver_matching/', include('driver_matching.urls')),
    path('payments/', include('payments.urls')),  
    path('reviews/', include('reviews.urls')),  
    path('tracking/', include(tracking_urls)),  
    path('trips/', include('trips.urls')),
]

# ✅ Ensure media files are served during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
