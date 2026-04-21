from django.urls import path
from . import views

urlpatterns = [
    path('one/', views.booking, name='startbooking'),
    path('two/', views.submitbooking, name='submitbooking'),
]