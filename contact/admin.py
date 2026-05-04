from django.contrib import admin
from .models import Contact

# Register your models here.

@admin.action(description="Mark as read")
def mark_read(modeladmin, request, queryset):
    """ Enables admin user to update instances of :model:`Contact` to `read` by bulk action. """
    queryset.update(read = True)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    Renders all instances of the :model:`Contact` in the admin panel.
    
    Contact messages can be marked as `read`
    """
    list_display = ('comment', 'read',)
    list_filter=('read',)
    actions=[mark_read]