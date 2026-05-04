from datetime import datetime, timedelta
from django.contrib import messages
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.views import generic
from .models import Workshop, WorkshopType
from bookings.models import Reservation, Feedback
from bookings.views import update_workshop_numbers, update_publication_status

# Create your views here.

class WorkshopList(generic.ListView):
    """
    Renders a paginated list of all workshops with the open publication status as well as a 
    gallery of images to encourage views to book

    Displays a list of all instances of the :model:`workshops.Workshop` with `publication_status=1`
    
    **Context**
    ``workshop_list`` 
    All workshops open for bookings

    **Template**
    :template: `workshop_list.html`
    """    
    queryset = Workshop.objects.filter(publication_status = 1)
    paginate_by = 6
    template_name = "workshop_list.hmtl"

    def get_context_data(self, **kwargs):
        # checks workshop numbers are up to date. Corrects for any bookings or adjustments done via 
        # the back end.  Ensures correct stock levels are displayed (eg. low stock or sold out)
        update_workshop_numbers()
        # checks against today's date whether a workshop session should be closed or cancelled.
        update_publication_status()
        context = super().get_context_data(**kwargs)
        return context

class ChildrensWorkshopList(generic.ListView):
    """
    Renders a paginated list of all workshops suitable for children with the open publication status as well as a 
    gallery of images to encourage views to book

    Displays a list of all instances of the :model:`workshops.Workshop` with `publication_status=1` and 
    `category__target_audience = CH`
    
    **Context**
    ``workshop_list`` 
    All children's workshops open for bookings

    **Template**
    :template: `workshop_list.html`
    """
    model= Workshop
    def get_queryset(self):
        return super().get_queryset().filter(category__target_audience ="CH", publication_status=1)
    paginate_by = 6
    template_name= "workshop_list.html" 

class FamilyWorkshopList(generic.ListView):
    """
    Renders a paginated list of all workshops suitable for families with the open publication status as well as a 
    gallery of images to encourage views to book

    Displays a list of all instances of the :model:`workshops.Workshop` with `publication_status=1` and 
    `category__target_audience = FA`
    
    **Context**
    ``workshop_list`` 
    All family workshops open for bookings

    **Template**
    :template: `workshop_list.html`
    """
    model= Workshop
    def get_queryset(self):
        return super().get_queryset().filter(category__target_audience ="FA", publication_status=1)
    paginate_by = 6
    template_name= "workshop_list.html" 

class AdultWorkshopList(generic.ListView):
    """
    Renders a paginated list of all workshops suitable for adults with the open publication status as well as a 
    gallery of images to encourage views to book

    Displays a list of all instances of the :model:`workshops.Workshop` with `publication_status=1` and 
    `category__target_audience = AD`
    
    **Context**
    ``workshop_list`` 
    All adult's workshops open for bookings

    **Template**
    :template: `workshop_list.html`
    """
    model= Workshop
    def get_queryset(self):
        return super().get_queryset().filter(category__target_audience ="AD", publication_status=1)
    paginate_by = 6
    template_name= "workshop_list.html" 

class WorkshopDetailView(generic.DetailView):
    """
    Renders details of a single instance of the :model:`workshops.Workshop` as well as displaying recent approved
    customer feedback and FAQs
    
    **Context**
    ``workshop`` 
    All fields of the workshop category

    ``feedback``
    The six most recently updated instances of approved feedback submitted by customers

    **Template**
    :template: `workshop_detail.html`
    """
    model= Workshop
    queryset = Workshop.objects.filter(publication_status =1)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feedback'] = Feedback.objects.filter(approved = True).order_by("-updated_on")[:6]
        return context