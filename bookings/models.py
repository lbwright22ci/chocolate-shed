from django.db import models
from django.contrib.auth.models import User
from workshops.models import Workshop

# Create your models here.

class Reservation(models.Model):

    """ Stores details of a single reservation related to both :model: `Workshop` and :model: `auth.user`"""

    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name='session_to_attend')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "bookee")
    adult_tickets = models.IntegerField(verbose_name='Number of adult places booked')
    child_tickets = models.IntegerField(verbose_name ='Number of child places booked')
    created_on = models.DateTimeField(auto_now_add= True)
    updated_on = models.DateTimeField(auto_now= True)
    paid = models.BooleanField(default = False)
    feedbackSubmitted = models.BooleanField(default = False)
    additional_information = models.TextField(blank=True)
    consent_given = models.BooleanField(default = False)

    class Meta:
        ordering= ["-updated_on"]
    def __str__(self):
        return f"Booking by {self.customer} for {self.workshop.category} on {self.workshop.event_date}"
