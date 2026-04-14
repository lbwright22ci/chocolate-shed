from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Workshop, WorkshopType, WorkshopActivity

# Register your models here.

admin.site.register(WorkshopType)
""" Renders all instances of :model:`WorkshopType` in admin panel"""

@admin.register(WorkshopActivity)
class WorkshopActivityAdmin(SummernoteModelAdmin):
    """ Renders all instances of :model:`WorkshopActivity` in the admin panel"""
    summernote_fields =('full_description')

@admin.register(Workshop)
class WorkshopAdmin(SummernoteModelAdmin):
    """ Renders all instances of :model:`Workshop` in admin panel 
    
    """
    list_filter = ('publication_status', 'category')
    search_fields =('event_date', 'title')
    


