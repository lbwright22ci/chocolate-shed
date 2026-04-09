from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Workshop

# Create your views here.

def WorkshopList(generic.ListView):
    queryset = Workshop.ojects.filter(status = 1)
    paginate_by = 6
    template_name = workshop/home.hmtl
