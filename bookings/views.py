from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from .models import Reservation
from .forms import WorkshopActivityForm, ReservationForm

# Create your views here.

# def booking(request):
#     return HttpResponse("this page is working")

# def submitBooking(request):
#     return HttpResponse("this page is working")

def booking(request):

    form_one = WorkshopActivityForm()

    if request.method == 'POST' :
        form_one = WorkshopActivityForm(data=request.POST)
        if form_one.is_valid():
            workshop_name = request.POST.get('activity')
            request.session['workshop_name'] = workshop_name

            return redirect('submitbooking')

    return render(
        request,
        "bookings/step-one.html",
        {"booking_form":form_one, },
    )

def submitbooking(request):
    workshop_name = request.session.get('workshop_name')
    print(workshop_name)

    form_two = ReservationForm(workshop_name=request.session.get('workshop_name'))
    if request.method =="POST":
        form_two = ReservationForm(data=request.POST, workshop_name= request.session.get('workshop_name'))
        if form_two.is_valid():
            # need to check if enough tickets are available here
            reservation = form_two.save(commit=False)
            reservation.customer = request.user
            reservation.save()


    return render(
        request,
        'bookings/step-two.html',
        {'booking_form':form_two,},
    )
