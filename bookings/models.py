from django.db import models
from django.contrib.auth.models import User
from workshops.models import Workshop

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    newsletter_consent = models.BooleanField(default=False)
    staff_status =models.BooleanField(default = False)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Reservation(models.Model):

    """ Stores details of a single reservation related to both :model: `Workshop` and :model: `auth.User`"""

    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name='workshop')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "customer")
    tickets = models.IntegerField( verbose_name ="Number of tickets to reserve")
    created_on = models.DateTimeField(auto_now_add= True)
    updated_on = models.DateTimeField(auto_now= True)
    paid = models.BooleanField(default = False)
    feedbackSubmitted = models.BooleanField(default = False)
    has_dietary_requirements = models.BooleanField(default=False, verbose_name="None of those attending have specific dietary needs or allergies")
    additional_information = models.TextField(blank=True, verbose_name="If 'no' above, please give details of any allergies (eg. latose, gluten, nuts) or dietary requirements (eg. vegan, Halal, vegetarian)")
    consent_given = models.BooleanField(default = False, verbose_name="I agree to the terms and conditions of booking and have supplied accurate information about the dietary needs and allergies for those attending")

    class Meta:
        ordering= ["-updated_on"]

    def __str__(self):
        return f"Booking by {self.customer} for {self.workshop.category} on {self.workshop.event_date}"
