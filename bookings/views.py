from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from workshops.models import Workshop
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
            if(Workshop.objects.filter(pk=int(request.POST.get('activity')), publication_status = 1).count() == 0):
               messages.error (request, 'Sorry there are no dates available for this activity at the moment')
            else:
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

    form_two = ReservationForm(workshop_name=request.session.get('workshop_name'))

    if request.method =="POST":
        form_two = ReservationForm(data=request.POST, workshop_name= request.session.get('workshop_name'))
        if form_two.is_valid():
            workshop_pending = Workshop.objects.get(pk=request.POST.get('workshop'))
            print (workshop_pending.tickets_sold, workshop_pending.max_places, type(int(request.POST.get('tickets'))), int(request.POST.get('tickets')))
            # need to check if enough tickets are available here
            if int(request.POST.get('tickets')) <= workshop_pending.max_places - workshop_pending.tickets_sold:
                reservation = form_two.save(commit=False)
                reservation.customer = request.user
                reservation.save()
                messages.success(request, 'booking made!')
            else:
                messages.error(request, f'Sorry there are only { workshop_pending.max_places - workshop_pending.tickets_sold } tickets left')

    return render(
        request,
        'bookings/step-two.html',
        {'booking_form':form_two,},
    )
