from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Workshop, WorkshopType

# Register your models here.

admin.site.register(WorkshopType)

@admin.register(Workshop)
class WorkshopAdmin(SummernoteModelAdmin):
    prepopulated_fields = {'slug':('event_date',)}
    summernote_fields =('excerpt', 'full_description')
    list_filter = ('publication_status', 'category')
    search_fields =('event_date', 'title')


