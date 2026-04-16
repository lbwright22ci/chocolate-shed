from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Contact
from .forms import ContactForm


# Create your views here.
def contact_us(request):
    
    if request.method == "POST":
        contact_form = ContactForm(data=request.POST)
        if contact_form.is_valid():
            contact_form.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Thank you for contacting The Chocolate Shed.  We will be in touch as soon as possible.  Please check your "spam" or "junk" folder if you have not heard from us within 2 working days.'
            )

    contact_form = ContactForm()

    return render(
        request,
        "contact/contact.html",
         {
          "contact_form":contact_form,
          },
    )
