from django.db import models

# Create your models here.
class Contact(models.Model):
    """ Stores single contact form submission entry
    
    Model fields are: `name`, `email`, `comment`, `read` and `created_on`
    """
    name = models.CharField(max_length=200)
    email = models.EmailField()
    comment = models.TextField()
    read = models.BooleanField(default=False)
    created_on= models.DateTimeField(auto_now=True)

    class Meta:
        ordering =["created_on"]
        # corrects the plural name for this model when displayed in admin panel.
        verbose_name_plural = "messages"

    def __str__(self):
        return f"Contact request from {self.name}"
    
