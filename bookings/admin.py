from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Reservation, UserProfile, Feedback

# Register your models here.

@admin.register(Reservation)
class Reservation(admin.ModelAdmin):
    list_display=('customer__email', 'workshop__activity__session_name', 'workshop__event_date', 'tickets', 'has_dietary_requirements')
    list_filter=('workshop__publication_status',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user__first_name', 'user__last_name', 'newsletter_consent', 'staff_status')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display =('booking__workshop__event_date','approved', 'feedback_rating', 'recommend' )
    list_filter =('submitted',)
