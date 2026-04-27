from datetime import datetime, timedelta, timezone
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from workshops.models import Workshop
from .models import Reservation, UserProfile
from .forms import WorkshopActivityForm, ReservationForm, UserProfileForm

# Create your views here.

def my_account(request):
    current_user = UserProfile.objects.get(user__id = request.user.id)
    print (current_user.newsletter_consent)
    sessions_attended = Reservation.objects.filter(customer = request.user, workshop__publication_status = 3).count()
    sessions_pending = Reservation.objects.filter(customer = request.user, workshop__publication_status = 1).count()
    return render(
        request,
        "bookings/my_account.html",
        {
         "current_user": current_user,
         "sessions_attended": sessions_attended,
         "sessions_pending":sessions_pending
        },
    )

def update_mailing(request):
    userprofile = UserProfile.objects.get(user__id = request.user.id)

    form = UserProfileForm(instance=userprofile)

    if request.method == 'POST':
        form = UserProfileForm(data=request.POST)
        if form.is_valid():
            temp = request.POST.get('newsletter_consent')
            
            if temp == "on":
                userprofile.newsletter_consent = True
            else:
                userprofile.newsletter_consent = False
            userprofile.save()
            
            messages.success(request, 'Mailing list preferences updated!')
            return redirect('my_account')
        else:
            messages.error(request, 'There was an error updating your mailing details')
    return render(
        request,
        'bookings/newsletter_update.html',
        {"form":form,
        },
        )


def booking(request):

    form_one = WorkshopActivityForm()

    if request.method == 'POST' :
        form_one = WorkshopActivityForm(data=request.POST)
        if form_one.is_valid():
            if(Workshop.objects.filter(activity=int(request.POST.get('activity')), publication_status = 1).count() == 0):
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
    
    for wp in Workshop.objects.all():
        wp_total = Reservation.objects.filter(workshop=wp).aggregate(tot=Sum('tickets'))['tot']

        if wp_total:
            wp.tickets_sold = wp_total
        else:
            wp.tickets_sold = 0
        wp.save()

    if request.method =="POST":
        form_two = ReservationForm(data=request.POST, workshop_name= request.session.get('workshop_name'))
        if form_two.is_valid():
            workshop_pending = Workshop.objects.get(pk=request.POST.get('workshop'))
            #if booked on a family workshop there needs to be at least 2 tickets reserved: one for child, one for adult
            if not ( workshop_pending.category.target_audience == 'FA' and int(request.POST.get('tickets')) == 1):

                # need to check if enough tickets are available here
                if int(request.POST.get('tickets')) <= workshop_pending.max_places - workshop_pending.tickets_sold:
                    reservation = form_two.save(commit=False)
                    reservation.customer = request.user
                    reservation.save()
                    messages.success(request, 'booking made!')
                    #update number of tickets sold on this workshop
                    workshop_pending.tickets_sold = workshop_pending.tickets_sold + int(request.POST.get('tickets'))
                    workshop_pending.save()

                    return redirect('my_bookingsList')
                else:
                    messages.error(request, f'Sorry there are only { workshop_pending.max_places - workshop_pending.tickets_sold } tickets left')
            else:
                messages.error(request, "The minimum booking for a family workshop is two: one adult & one child")
        else:
            messages.error(request, "There was an error submitting this form")

    return render(
        request,
        'bookings/step-two.html',
        {'booking_form':form_two,},
    )

class my_bookingsList(generic.ListView):

    model = Reservation
    template_name = 'bookings/my_bookings.html'
    

    def get_queryset(self):
        return super().get_queryset().filter(customer = self.request.user)
    
def staff_page(request):
    workshopList = Workshop.objects.filter(publication_status = 1)
    bookings = Reservation.objects.filter(workshop__publication_status = 1)
    current_user = UserProfile.objects.get(user__id = request.user.id)

    return render(
        request,
        'bookings/staff_info.html',
        {"workshopList": workshopList,
         "bookings": bookings,
         "current_user": current_user,
         },
    )