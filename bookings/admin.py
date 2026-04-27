from django.contrib import admin
from datetime import datetime
from django_summernote.admin import SummernoteModelAdmin
from .models import Reservation, UserProfile, Feedback

# Register your models here.

admin.site.register(Reservation)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user__first_name', 'user__last_name', 'newsletter_consent', 'staff_status')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display =('booking__workshop__event_date','approved', 'feedback_rating', 'recommend' )
    list_filter =('submitted',)

#Mix reservation and feedback info
class FeedbackInline(admin.StackedInline):
    model = Feedback

class BookingAdmin(admin.ModelAdmin):
    model = Reservation
    inlines =[FeedbackInline]

admin.site.unregister(Reservation)

admin.site.register(Reservation, BookingAdmin)