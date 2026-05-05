from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from cloudinary.models import CloudinaryField


# Create your models here.

class WorkshopType(models.Model):
    """
    Stores a single workshop category (eg. kids, 1 hour workshop,
    costing £27.50 pp)

    Model fields are: `target_audience`, `workshop_duration` and
    `workshop_price`.
    This model is a Foriegn Key of :model:`Worshop`
    """
    # Holds target audience options for workshop sessions
    TYPE_CHOICES = (
        ('CH', 'children'),
        ('AD', 'adults'),
        ('FA', 'families')
    )

    target_audience = models.CharField(max_length=2, choices=TYPE_CHOICES)
    workshop_duration = models.IntegerField(
        verbose_name="Workshop duration (min)")
    workshop_price = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name="Cost pp (£)")

    class Meta:
        ordering = ["target_audience"]

    def __str__(self):
        return f"{self.workshop_duration} min {self.get_target_audience_display()}"


class WorkshopActivity(models.Model):
    """ Stores generic workshop information for sessions which
      have the same activity.

    The fields of this model are `session_name`, `excerpt` and
      `full_description`.
    This model is a Foriegn key to :model:`Worshop`
    """
    session_name = models.CharField(max_length=100)
    excerpt = models.CharField(max_length=150)
    full_description = models.TextField()

    class Meta:
        # corrects pluralisation of this model.
        verbose_name_plural = "workshop activities"

    def __str__(self):
        return f"{self.session_name}"


class Workshop(models.Model):
    """ Stores a single workshop entry related to
      :model:`WorkshopCategory`
    and :model: `WorkshopActivity`

    The fields of this model are `category`, `activity`, `event_date`,
      `location`, `max_places`,
    `primary_photo`, `updated_on`, `publication_status`, `slug`,
      `tickets_sold` and `low_stock`.
    Images are hosted by Cloudinary and should be compressed to webp
      format prior to uploading via
    the admin panel.
    """
    # holds options for publication status of a workshop.  Cancelled
    # workshops are those with no
    # bookings when the event date is less than 3 weeks from the current date.
    STATUS = ((0, 'Draft'), (1, 'Open'), (2, 'Cancelled'), (3, 'Closed'))

    category = models.ForeignKey(
        WorkshopType, on_delete=models.CASCADE, related_name='category')
    activity = models.ForeignKey(
        WorkshopActivity, on_delete=models.CASCADE, related_name='activity')
    event_date = models.DateTimeField(unique=True)
    location = models.CharField(max_length=400, default='on site')
    max_places = models.IntegerField(default=12)
    primary_photo = CloudinaryField(
        'cover_image', default='placeholder_workshop')
    updated_on = models.DateField(auto_now=True)
    publication_status = models.IntegerField(choices=STATUS, default=0)
    slug = models.SlugField(max_length=200, unique=True)
    tickets_sold = models.IntegerField(default=0)
    low_stock = models.BooleanField(default=False)

    class Meta:
        ordering = ['event_date']

    def __str__(self):
        return f"{self.activity.session_name} for {self.category.get_target_audience_display()} {self.event_date.strftime("%d-%b-%y %H:%M")}"
