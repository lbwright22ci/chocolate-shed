from django.urls import path
from . import views

urlpatterns = [
    path('one/', views.booking, name='startbooking'),
    path('two/', views.submitbooking, name='submitbooking'),
    path('my_bookings/', views.my_bookingsList.as_view(), name="my_bookingsList"),
]