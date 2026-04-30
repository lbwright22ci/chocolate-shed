from datetime import datetime, timedelta
from django.shortcuts import render
from django.views import generic
from django.db.models import Sum
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils import timezone
from .models import Workshop, WorkshopType
from bookings.models import Reservation, Feedback
from bookings.views import update_workshop_numbers, update_publication_status

# Create your views here.

class WorkshopList(generic.ListView):    
    queryset = Workshop.objects.filter(publication_status = 1)
    paginate_by = 6
    template_name = "workshop_list.hmtl"

    def get_context_data(self, **kwargs):
        update_workshop_numbers()
        update_publication_status()
        context = super().get_context_data(**kwargs)
        return context

class ChildrensWorkshopList(generic.ListView):
    model= Workshop
    def get_queryset(self):
        return super().get_queryset().filter(category__target_audience ="CH", publication_status=1)
    paginate_by = 6
    template_name= "workshop_list.html" 

class FamilyWorkshopList(generic.ListView):
    model= Workshop
    def get_queryset(self):
        return super().get_queryset().filter(category__target_audience ="FA", publication_status=1)
    paginate_by = 6
    template_name= "workshop_list.html" 

class AdultWorkshopList(generic.ListView):
    model= Workshop
    def get_queryset(self):
        return super().get_queryset().filter(category__target_audience ="AD", publication_status=1)
    paginate_by = 6
    template_name= "workshop_list.html" 

class WorkshopDetailView(generic.DetailView):
    model= Workshop
    queryset = Workshop.objects.filter(publication_status =1)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feedback'] = Feedback.objects.filter(approved = True).order_by("-updated_on")[:6]
        return context