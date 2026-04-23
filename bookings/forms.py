from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Reservation
from workshops.models import Workshop, WorkshopActivity, WorkshopType

class CustomSignupForm(forms.Form):
    first_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    newsletter_consent = forms.BooleanField()

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        profile = UserProfile(user=user)
        profile.newsletter_consent = self.cleaned_data.get('newsletter_consent', False)
        profile.save()

class WorkshopActivityForm(forms.ModelForm):
    class Meta:
        model = Workshop
        fields = ['activity']
    
class ReservationForm(forms.ModelForm):
    class Meta: 
        model = Reservation
        fields = ['workshop', 'tickets', 'has_dietary_requirements', 'additional_information', 'consent_given']
    def __init__(self, *args, **kwargs):
        workshop_name = kwargs.pop('workshop_name')
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields['workshop'].queryset = Workshop.objects.filter(activity = workshop_name, publication_status =1)
        self.fields['additional_information'].widget = forms.Textarea(attrs={'rows':4})