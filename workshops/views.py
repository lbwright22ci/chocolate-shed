from datetime import datetime, timedelta
from django.shortcuts import render
from django.views import generic
from django.db.models import Sum
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils import timezone
from .models import Workshop, WorkshopType
from bookings.models import Reservation, Feedback

# Create your views here.

class WorkshopList(generic.ListView):


    for wp in Workshop.objects.all():
        wp_total = Reservation.objects.filter(workshop=wp).aggregate(tot=Sum('tickets'))['tot']

        if wp_total:
            wp.tickets_sold = wp_total
        else:
            wp.tickets_sold = 0
        wp.save()
        
    for wp in Workshop.objects.filter(publication_status=1):
        if wp.tickets_sold > (wp.max_places - 3) :
            wp.low_stock = True
            wp.save()
        else:
            wp.low_stock = False
            wp.save()
        if wp.event_date < timezone.now()-timedelta(days=2):
            wp.publication_status = 3
            wp.save()
        elif wp.tickets_sold == 0:
            if wp.event_date < timezone.now()-timedelta(days=21):
                wp.publication_status = 2
                wp.save()
    
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
    queryset = Workshop.objects.filter(publication_status =1)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feedback'] = Feedback.objects.filter(approved = True).order_by("-updated_on")[:6]
        return context