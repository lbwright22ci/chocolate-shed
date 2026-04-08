from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.

class WorkshopType(models.Model):
    
    """ Stores a single workshop category (eg. kids, 1 hour workshop, costing £27.50 pp)"""

    TYPE_CHOICES =(
        ('CH', 'mixed ages 8-16 years'),
        ('AD', 'adults & late teens'),
        ('FA', 'children with adults')
    )

    target_audience= models.CharField(max_length=2, choices = TYPE_CHOICES)
    workshop_duration = models.IntegerField(verbose_name="Workshop duration (min)")
    workshop_price = models.DecimalField(max_digits = 6, decimal_places=2, verbose_name ="Cost pp (£)")

    class Meta:
        ordering = ["target_audience"]
    
    def __str__(self):
        return f"{self.workshop_duration} minute workshop for {self.get_target_audience_display()}"

class Workshop(models.Model):
    """ Stores a single workshop entry related to :model:`WorkshopCategory`"""

    STATUS = ( (0, 'Draft'), (1, 'Open'), (2, 'Cancelled'), (3, 'Closed'))

    category = models.ForeignKey(WorkshopType, on_delete=models.CASCADE, related_name= 'category')
    event_date = models.DateTimeField(unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    session_name = models.CharField(max_length=200)
    location = models.CharField(max_length=400, default='on site')
    excerpt = models.TextField(max_length= 500)
    full_description = models.TextField()
    max_places = models.IntegerField(default = 12)
    primary_photo = CloudinaryField('cover_image', default ='placeholder_workshop' )
    secondary_photo = CloudinaryField('extra_image', blank = True)
    updated_on = models.DateField(auto_now= True)
    publication_status = models.IntegerField(choices = STATUS, default = 0)

    class Meta:
        ordering = ['-event_date']

    def __str__(self):
        return f"{self.event_date} workshop for {self.category}"
