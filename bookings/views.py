
from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.views import generic
from workshops.models import Workshop
from .models import Reservation, UserProfile, Feedback
from .forms import WorkshopActivityForm, ReservationForm, UserProfileForm, FeedbackForm

# Create your views here.

def update_workshop_numbers():
    for wp in Workshop.objects.all():
        wp_total = Reservation.objects.filter(workshop=wp).aggregate(tot=Sum('tickets'))['tot']
        if wp_total:
            wp.tickets_sold = wp_total
        else:
            wp.tickets_sold = 0
        if wp.tickets_sold > wp.max_places - 3:
            wp.low_stock = True
        else:
            wp.low_stock = False
        wp.save()

def update_publication_status():
    for wp in Workshop.objects.filter(publication_status=1):
        if wp.event_date < timezone.now()+timedelta(days=21) and wp.tickets_sold == 0:
            wp.publication_status = 2
            wp.save()
        elif wp.event_date < timezone.now()+timedelta(days=2):
            wp.publication_status = 3
            wp.save()

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
    update_workshop_numbers()
    update_publication_status()

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
    
    update_workshop_numbers()
    update_publication_status()

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
                    if workshop_pending.tickets_sold > workshop_pending.max_places-3:
                        workshop_pending.low_stock = True
                    else:
                        workshop_pending.low_stock= False
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

def update_booking(request, id):
    original_booking = Reservation.objects.get(id = id)
    customer = original_booking.customer
    temp = original_booking.tickets

    update_workshop_numbers()
    update_publication_status()

    form = ReservationForm(workshop_name=original_booking.workshop.activity, instance = original_booking)

    if request.method =="POST":
        form = ReservationForm(data=request.POST, workshop_name=original_booking.workshop.activity, instance = original_booking)
        if form.is_valid():
            #variables collected by the request
            tickets_requested = int(request.POST.get('tickets'))
            ticket_difference = tickets_requested - temp
            
            workshop_pending = Workshop.objects.get(pk=request.POST.get('workshop'))
            
            #if booked on a family workshop there needs to be at least 2 tickets reserved: one for child, one for adult
            if not ( workshop_pending.category.target_audience == 'FA' and tickets_requested == 1):
                
                # need to check if enough tickets are available here
                if ticket_difference <= workshop_pending.max_places - workshop_pending.tickets_sold:
                    original_booking =form.save(commit=False)
                    original_booking.save()
                    messages.success(request, 'Booking updated!')
                    #update number of tickets sold on this workshop
                    workshop_pending.tickets_sold = workshop_pending.tickets_sold + ticket_difference
                    if workshop_pending.tickets_sold > workshop_pending.max_places-3:
                        workshop_pending.low_stock = True
                    else:
                        workshop_pending.low_stock= False
                    workshop_pending.save()
                    return redirect('my_bookingsList')
                else:
                    messages.error(request, f'Sorry there were only { workshop_pending.max_places - workshop_pending.tickets_sold } tickets left for this session and you requested { ticket_difference } extra places')
                    
            else:
                messages.error(request, "The minimum booking for a family workshop is two: one adult & one child")
        else:
            messages.error(request, "There was an error submitting this form")


    return render(
        request,
        "bookings/update_booking.html",
        {"form":form,
         "customer": customer,
         "original_booking":original_booking,},
    )

def delete_booking(request, id):
    booking = get_object_or_404(Reservation, pk=id)
    wk = booking.workshop
    tk = booking.tickets

    if booking.customer == request.user:
        booking.delete()
        #return tickets canceled back to the workshop total available:
        wk.tickets_sold = wk.tickets_sold - tk
        if wk.tickets_sold > wk_pending.max_places-3:
            wk.low_stock = True
        else:
            wk.low_stock= False
        wk.save()
        messages.add_message(request, messages.SUCCESS, f'Your reservation for { wk } has been canceled.  We hope you see you soon at another event.')
    else:
        messages.add_message(request, messages.ERROR, 'You do not have access to cancel this booking')

    return HttpResponseRedirect(reverse('my_bookingsList'))

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

def feedback_page(request):
    current_user = UserProfile.objects.get(user__id = request.user.id)
    past_bookings = Reservation.objects.filter(customer = request.user.id, workshop__publication_status = 3)
    feedback_sorted = Feedback.objects.filter(booking__customer = request.user.id, booking__workshop__publication_status = 3)


    return render(
        request,
        'bookings/leave_feedback.html',
        {"current_user": current_user,
         "past_bookings": past_bookings,
         "feedback_sorted": feedback_sorted,
          },
    )

def delete_feedback(request, id):
    review = Feedback.objects.get(pk = id)
    review.feedback_comment= " "
    review.feedback_rating =0
    review.approved = False
    review.submitted = False
    review.recommend = False
    review.save()
    messages.add_message(request, messages.SUCCESS, "Your feedback for this workshop has been removed.")

    return HttpResponseRedirect(reverse('feedback_page'))

def feedback_form(request, id):
    review = Feedback.objects.get(booking__id = id)
    form = FeedbackForm(instance=review)

    if request.method == "POST":
        form = FeedbackForm(data=request.POST, instance = review)
        if form.is_valid:
            temp = request.POST.get('recommend')
            if temp == "on":
                review.recommend = True
            else:
                review.recommend = False
            review.feedback_comment = request.POST.get('feedback_comment')
            review.feedback_rating = request.POST.get('feedback_rating')
            review.submitted = True
            review.approved = False
            review.save() 
            messages.success(request, 'Thank you for leaving feedback!')
            return redirect ('feedback_page')
        else:
            messages.error(request, 'form not valid')


    return render(
        request,
        'bookings/feedback.html',
        {"form":form,
         "review": review,},
    )