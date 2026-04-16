from django.contrib import admin
from .models import Contact

# Register your models here.
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    Makes submissions of :form:`contact.ContactForm` visible to superUser in the admin pannel
    User can update :model:`contact.Contact.read` field
    """
    list_display = ('comment', 'read',)
    list_filter=('read',)