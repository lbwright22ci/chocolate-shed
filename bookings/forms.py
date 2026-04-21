from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Reservation
from workshops.models import Workshop, WorkshopActivity, WorkshopType

class CustomSignupForm(forms.Form):
    newsletter_consent = forms.BooleanField()
    def signup(self, request, user):

        user.save()
        profile = UserProfile(user=user)
        profile.newsletter_consent = self.cleaned_data.get('newsletter_consent', False)
        profile.save()


class step_one(forms.Form):
    first_name = forms.CharField(max_length= 20, widget= forms.TextInput(attrs={'placeholder': 'First name'})
    )
    last_name = forms.CharField(max_length= 20, widget= forms.TextInput(attrs={'placeholder': 'Last name'})
    )
    workshop_name = forms.ModelChoiceField(queryset=WorkshopActivity.objects.all())

    def add_user(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        
#class step_two(forms.Form):


    # def start_booking(self, request, user):
    #     user.first_name = self.cleaned_data['first_name']
    #     user.last_name = self.cleaned_data['last_name']
    #     user.save()
    #     request.session()
    # workshop_date = forms.ModelChoiceField(queryset=Workshop.objects.filter(activity__session_name = 'workshop_name'))
    
    # #if Workshop.objects.get(activity.session_name == 'workshop_name').count() > 1:
    #     workshop_date = forms.ModelChoiceField(queryset= Workshop.event_date.filter(activity.session_name == 'workshop_name'))
    # else:
    #     workshop_date = Workshop.objects.get(activity.session_name == "workshop_name").event_date
    

    # class Meta:
    #     model= Reservation
    #     fields =('workshop', 'adult_tickets', 'child_tickets', 'additional_information', 'consent_given',)