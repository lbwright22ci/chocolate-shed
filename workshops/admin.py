from django.contrib import admin
from .models import Workshop, WorkshopType

# Register your models here.

admin.site.register(WorkshopType)

admin.site.register(Workshop)

