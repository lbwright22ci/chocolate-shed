from django.contrib import admin
from datetime import datetime
from django_summernote.admin import SummernoteModelAdmin
from .models import Reservation

# Register your models here.

@admin.register(Reservation)
class ReservationAdmin(SummernoteModelAdmin):
    """"Renders all instances of :model:`bookings.Reservation` in the admin panel
    """
    list_display = ('workshop__event_date', 'customer__email', 'tickets', 'has_dietary_requirements')
