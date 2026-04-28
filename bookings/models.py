from django.db import models
from datetime import datetime
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from workshops.models import Workshop


RATING = ((0, 'not specified'), (1, 'Terrible'), (2, 'Disappointing'), (3, 'Average'), (4, 'Enjoyed it!'), (5, 'Brilliant!'))

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
    has_dietary_requirements = models.BooleanField(default=False, verbose_name="Members of my booking have specific dietary needs or allergies")
    additional_information = models.TextField(blank=True, verbose_name="If 'yes' above, please give details of any allergies (eg. latose, gluten, nuts) or dietary requirements (eg. vegan, Halal, vegetarian)")
    consent_given = models.BooleanField(default = False, verbose_name="I agree to the terms and conditions of booking and have supplied accurate information about the dietary needs and allergies for those attending")

    class Meta:
        ordering= ["workshop__event_date"]

    def __str__(self):
        return f"Booking by {self.customer} for {self.workshop.category} on {self.workshop.event_date.strftime("%d-%b-%y %H:%M")}"

class Feedback(models.Model):
    booking = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name ='booking')
    feedback_rating = models.IntegerField(choices=RATING, default=0)
    feedback_comment = models.TextField(blank=True)
    recommend = models.BooleanField(default=False, verbose_name='I would recommend this to others.')
    updated_on = models.DateField(auto_now=True)
    approved = models.BooleanField(default=False)
    submitted = models.BooleanField(default=False)

    class Meta:
        ordering=["-booking__workshop__event_date"]
        verbose_name_plural= "feedback"

    def __str__(self):
        return f"Feedback by {self.booking.customer} for {self.booking.workshop.category}"
    
#create booking Feedback by default when booking is made:
def create_feedback(sender, instance, created, **kwargs):
    if created:
        reservation_feedback = Feedback(booking=instance)
        reservation_feedback.save()

post_save.connect(create_feedback, sender=Reservation)