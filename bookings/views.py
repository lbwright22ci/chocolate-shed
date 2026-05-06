
from datetime import datetime, timedelta, timezone
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils import timezone
from django.views import generic
from workshops.models import Workshop
from .models import Reservation, UserProfile, Feedback
from .forms import WorkshopActivityForm, ReservationForm, UserProfileForm, FeedbackForm

# Create your views here.

def update_workshop_numbers():
    """
    Updates the `tickets_sold` field of the :model:`workshops.Workshop`, taking in to account orders
    added through the back end as well as front end.

    Updates the `low_stock` field of the :model:`workshops.Workshop` as reservations are made, canceled or
    updated through either the front or back end of the website.

    **Business logic**
    An instance of the :model:`workshops.Workshop` has `low_stock` if there are 3 or less tickets available for sale.
    """
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
    """
    Checks the publication status of every instance of :model:`worshops.Workshop` is up to date
    
    **Business Logic**
    Customer can only place reservations for `open` (`publication_status=1`) workshops
    `Open` worshops are marked as `closed` (`publication_status = 3`) two days prior to the event date
    to prevent last minute bookings
    `Open` workshops are marked as `cancelled` (`publication_status =2`) three weeks prior to the event 
    date if no bookings have been made up until that point to prevent loss making events.
    
    """
    for wp in Workshop.objects.filter(publication_status=1):
        if wp.event_date < timezone.now()+timedelta(days=21) and wp.tickets_sold == 0:
            wp.publication_status = 2
            wp.save()
        elif wp.event_date < timezone.now()+timedelta(days=2):
            wp.publication_status = 3
            wp.save()

def my_account(request):
    """
    Displays My account settings page for a user when logged in which includes 
    data from :model:`bookings.UserProfile`.

    **Context**

    ``current_user``
        An instance of :model:`bookings/UserProfile` related by OnetoOneField to :model:`auth.User`.
    ``sessions_attended``
        A count of past bookings for this user.
    ``sessions_pending``
        A count of future bookings for this user.

    **Template:**

    :template:`bookings/my_account.html`
    """
    current_user = UserProfile.objects.get(user__id = request.user.id)
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
    """
    Displays a single instance of the :form:`bookings.UserProfileForm` to allow a logged in user to 
    opt in or out of being on a mailing list.

    **Context**

    ``form``
        An instance of :forms:`bookings.UserProfileForm`

    **Template:**

    :template:`bookings/newsletter_update.html`
    """
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
    """
    Displays first stage of creating a new instance of the :model:`bookings.Reservation`.

    Stores `session_name` of the workshop user selects in the Django session variable labeled `workshop_name`
    before redirecting the user to :views:`submitbooking`.

    **Context**

    ``form_one``
        An instance of :form:`bookings.WorkshopActivityForm`.

    **Template:**

    :template:`bookings/step-one.html`
    """
    form_one = WorkshopActivityForm()

    #correct for any bookings which may have been placed through the back end for this workshop
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
    """
    Displays second stage of creating a new instance of the :model:`bookings.Reservation`.

    **Business Logic**
    - The dates for open workshops which match the `workshop_name` saved from stage one are shown only
    - Family workshops must have a minimum of two tickets reserved per booking (one adult and one child)
    - Bookings can only be made if there are enough tickets available.
    By JavaScript:
    - Customers must confirm they agree to T&Cs of booking for the form to be valid
    - Customers who state there are members of their group who have allergies must give further details

    **Context**

    ``booking_form``
        An instance of :form:`bookings.ReservationForm`.

    **Template:**

    :template:`bookings/step-two.html`
    """
    workshop_name = request.session.get('workshop_name')

    form_two = ReservationForm(workshop_name=request.session.get('workshop_name'))
    
    # updates number of available tickets and publication status of workshops in case changes have been 
    # made in the back end while moving from the first stage of the booking process.

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
    """
    Updates the instance of the :model:`bookings.Reservation` with `pk=id`.  Customers can change the date,
    number of tickets and allergies of their reservation. To change to a different activity they must cancel the
    booking and start again.

    **Business Logic**
    same business logic applied to submitbooking()

    **Context**

    ``form``
        An instance of :form:`bookings.ReservationForm` prefilled with data for `pk=id`.
    ``original_booking`` 
        Instance of :model:`bookings.Reservation` with pk=`id` prior to any changes being made
    ``customer``
        Instance of :model:`auth.Users` related to :model:`bookings.Reservation` with pk=`id`
    
    **Template:**

    :template:`bookings/update_booking.html`
    """
    original_booking = Reservation.objects.get(id = id)
    customer = original_booking.customer
    temp = original_booking.tickets

    #checks workshop numbers are up to date for any editing through the back end as well as front end. 
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
    """
    Deletes the instance of the :model:`bookings.Reservation` with `pk=id`.
    User is asked to confirm that they want to delete before proceeding.
    
    """
    booking = get_object_or_404(Reservation, pk=id)
    wk = booking.workshop
    tk = booking.tickets

    if booking.customer == request.user:
        booking.delete()
        #return tickets canceled back to the workshop total available:
        wk.tickets_sold = wk.tickets_sold - tk
        if wk.tickets_sold > wk.max_places-3:
            wk.low_stock = True
        else:
            wk.low_stock= False
        wk.save()
        messages.add_message(request, messages.SUCCESS, f'Your reservation for { wk } has been canceled.  We hope you see you soon at another event.')
    else:
        messages.add_message(request, messages.ERROR, 'You do not have access to cancel this booking')

    return HttpResponseRedirect(reverse('my_bookingsList'))

class my_bookingsList(generic.ListView):
    """
    Displays a list of all open bookings a customer has along with the option for them to easily update or cancel.

    **Context**

    ``reservation_list``
        List of all instances of the :model:`bookings.Reservation` with `workshop__publication_status`= 1 (open)
        related to the customer (the instance of :model:`auth.User` which is authenicated)
    
    **Template:**

    :template:`bookings/my_bookings.html`
    """
    model = Reservation
    template_name = 'bookings/my_bookings.html'

    def get_queryset(self):
        return super().get_queryset().filter(customer = self.request.user)
    
def staff_page(request):
    """
    Displays a list of all instances of :model:`workshops.Workshop` with `publication_status`=1 (open)
    Along with details of any instances :model:`bookings.Reservation` associated with each.
    Page is accessible to instances of :model:`bookings.UserProfile` with staff_status = True only

    **Context**

    ``workshop_list``
        List of all instances of the :model:`workshops.Workshop` with `workshop__publication_status`= 1 (open)
    ``bookings``
        All instances of :model:`bookings.Reservation`
    ``current_user``
        Instance of :model:`bookings.UserProfile` authenicated viewing the page.
    
    **Template:**

    :template:`bookings/staff_info.html`
    """
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
    """
    Displays a list of all closed bookings a customer has along with the option for them to easily leave or update feedback comments.

    **Context**

    ``past_bookings``
        List of all instances of the :model:`bookings.Reservation` with `workshop__publication_status`= 3 (closed) belonging to 
        the customer (the instance of :model:`auth.User` which is authenicated)
    ``feedback_sorted``
        All instances of the :model:`bookings.Feedback` with `booking__workshop__publication_status`= 3 (closed) belonging to 
        the customer (the instance of :model:`auth.User` which is authenicated)
    ``current_user``
        Instance of :model:`bookings.UserProfile` for the authenicated user.
    
    **Template:**

    :template:`bookings/leave_feedback.html`
    """
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
    """
    Removes comment, recommendation and rating submitted by a customer for instance of :model:`bookings.Feedback` 
    related to :model:`bookings.Rerservation`
    """
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
    """
    Displays instance of :form:`bookings.FeedbackForm` associated with :model:`booking.Feedback`

    **Business Logic**
    - When feedback is submitted by a customer, `submitted` is updated to `True`
    - After any update to feedback by customer, it is marked as `approved= False` to allow site owner to 
    read and moderate prior to publication.
    
    **Context**

    ``form``
        Instance of :form:`bookings.FeedbackForm` associated with instance of :model:`booking.Feedback` with pk=`id`
    ``review``
        Instance of :model:`booking.Feedback` with pk=`id`
    
    **Template:**

    :template:`bookings/feedback.html`
    """
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