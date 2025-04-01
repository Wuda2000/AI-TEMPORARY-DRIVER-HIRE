from django.urls import path
from . import views

urlpatterns = [
    # Example view
    path('', views.review_list, name='review_list'),
]
