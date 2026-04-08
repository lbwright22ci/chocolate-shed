from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Workshop, WorkshopType

# Register your models here.

admin.site.register(WorkshopType)
""" Renders all instances of :model:`WorkshopType` in admin panel"""

@admin.register(Workshop)
class WorkshopAdmin(SummernoteModelAdmin):
    """ Renders all instances of :model:`Workshop` in admin panel 
    
    """
    prepopulated_fields = {'slug': ('category', 'session_name')}
    summernote_fields =('excerpt', 'full_description')
    list_filter = ('publication_status', 'category')
    search_fields =('event_date', 'title')


