from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Workshop, WorkshopType, WorkshopActivity

# Register your models here.

@admin.register(WorkshopType)
class WorkshopTypeAdmin(admin.ModelAdmin):
    """ Renders all instances of :model:`WorkshopType` in admin panel"""
    list_display=('target_audience', 'workshop_duration', 'workshop_price')
    list_editable=('workshop_price', 'workshop_duration')


@admin.register(WorkshopActivity)
class WorkshopActivityAdmin(SummernoteModelAdmin):
    """ Renders all instances of :model:`WorkshopActivity` in the admin panel"""
    summernote_fields =('full_description')
    list_display=('session_name', 'excerpt')

@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    """ Renders all instances of :model:`Workshop` in admin panel """
    list_filter = ('publication_status', 'category')
    search_fields =('event_date', 'activity__session_name')
    list_display =('event_date', 'category__target_audience', 'activity__session_name', 'tickets_sold')


