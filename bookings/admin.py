from django.contrib import admin
from datetime import datetime
from django_summernote.admin import SummernoteModelAdmin
from .models import Reservation, UserProfile

# Register your models here.

@admin.register(Reservation)
class ReservationAdmin(SummernoteModelAdmin):
    """"Renders all instances of :model:`bookings.Reservation` in the admin panel
    """
    list_display = ('workshop__event_date', 'customer__first_name', 'customer__last_name', 'tickets', 'has_dietary_requirements', 'paid')

@admin.register(UserProfile)
class UserProfileAdmin(SummernoteModelAdmin):
    list_display = ('user__first_name', 'user__last_name', 'newsletter_consent', 'staff_status')