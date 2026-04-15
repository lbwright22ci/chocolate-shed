#from datetime import datetime, timedelta
from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Workshop, WorkshopType

# Create your views here.

# def update_workshop_status():
    # today = date.today()
    # cancellation_period = timedelta(days=21)
    # """ Updates publication status of a workshop to closed if the event date has passed"""
    # Workshop.ojects.filter(event_date <= today and publication_status == 1).update(publication_status = 3)
    # """ updates publication status of a workshop to cancelled if the event date is less than 3 weeks away 
    # and there are no bookings"""
    # workshop.ojects.filter(event_date -cancellation_period < today and session_to_attend.count() == 0).update(publication_status = 3)

class WorkshopList(generic.ListView):
    queryset = Workshop.objects.filter(publication_status = 1)
    paginate_by = 6
    template_name = "workshop_list.hmtl"

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
    queryset = Workshop.objects.filter(publication_status=1)