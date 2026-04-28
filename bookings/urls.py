from django.urls import path
from . import views

urlpatterns = [
    path('one/', views.booking, name='startbooking'),
    path('two/', views.submitbooking, name='submitbooking'),
    path('my_account/', views.my_account, name='my_account'),
    path('my_bookings/', views.my_bookingsList.as_view(), name="my_bookingsList"),
    path('my_bookings/<int:id>', views.update_booking, name="update_booking"),
    path('leave_feedback/', views.feedback_page, name = 'feedback_page'),
    path('feedback/<int:id>', views.feedback_form, name="feedback_form"),
    path('mailing_list/', views.update_mailing, name='update_mailing'),
    path('staff_info/', views.staff_page, name='staff_page'),
]