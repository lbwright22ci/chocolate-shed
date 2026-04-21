from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .models import Reservation
from .forms import step_one

# Create your views here.

def booking(request):

    booking_form = step_one()

    if request.method=='POST':
        booking_form = step_one(data=request.POST)
        if booking_form.is_valid():
            
            #user.first_name = request.POST.get('first_name')
            #user.last_name = request.POST.get('last_name')
            #user.save()
            workshop_name = request.POST.get('workshop_name')
            
            request.session['workshop_name'] = workshop_name

            return redirect('step_two')

    return render(
        request,
        "bookings/step-one.html",
        {"booking_form":booking_form, },
    )

def step_two(request):
    workshop_name = request.session.get('workshop_name')

    #check available dates
    dates = checkDates(workshop_name)


    return render(
        request,
        'bookings/step-one.html',
        {'booking_form':booking_form,},
    )

def checkDates(workshop_name):
    dates=[]
    for workshops in Workshop.objects.filter(activity__session_name= workshop_name):
        dates.append(workshop.event_date)
    return dates