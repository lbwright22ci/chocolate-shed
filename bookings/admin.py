from django.contrib import admin
from .models import Reservation, UserProfile, Feedback

# Register your models here.


@admin.action(description="Update payment status to paid")
def mark_paid(modeladmin, request, queryset):
    """ Enables admin user to update instances of :model:`Reservation`
      to `paid` by bulk action. """
    queryset.update(paid=True)


@admin.action(description="Approve feedback comment for publication")
def mark_approved(modeladmin, request, queryset):
    """ Enables admin user to update instances of :model:`Feedback` to
      `approved` by bulk action. """
    queryset.update(approved=True)


@admin.action(description="Give user staff status")
def make_staff(modeladmin, request, queryset):
    """ Enables admin user to update instances of :model:`UserProfile` to
      `staff` by bulk action. """
    queryset.update(staff_status=True)


@admin.register(Reservation)
class Reservation(admin.ModelAdmin):
    """
    Renders all instances of the :model:`Reservation` in the admin panel.

    Reservations or bookings can be marked as `paid`
    """
    list_display = ('customer__email', 'workshop__activity__session_name',
                    'workshop__event_date', 'tickets',
                    'has_dietary_requirements')
    list_filter = ('workshop__publication_status',)
    actions = [mark_paid]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Renders all instances of the :model:`UserProfile` in the admin
      panel.

    Users can be marked as `staff` which will give them access to
    the staff area on the website when logged in
    but not access to the Django admin panel.
    """
    list_display = ('user__first_name', 'user__last_name',
                    'newsletter_consent', 'staff_status')
    actions = [make_staff]


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """
    Renders all instances of the :model:`Feedback` in the admin panel.

    Feedback comments can be approved in bulk.Only approved comments
      will be published.
    """
    list_display = ('booking__workshop__event_date',
                    'approved', 'feedback_rating', 'recommend')
    list_filter = ('submitted',)
    actions = [mark_approved]
