from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from .models import UserProfile, Reservation, Feedback
from workshops.models import Workshop, WorkshopActivity, WorkshopType

RATING = ((1, 'Terrible'), (2, 'Disappointing'), (3, 'Average'), (4, 'Enjoyed it!'), (5, 'Brilliant!'))

class CustomSignupForm(forms.Form):
    """
    Customises AllAuth signup form to include the additional fields 'first name', last name' for :model:`auth.User`
    and 'newsletter_consent' for :model:`bookings.UserProfile`
    """
    first_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    newsletter_consent = forms.BooleanField(required = False)

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        profile = UserProfile(user=user)
        profile.newsletter_consent = self.cleaned_data.get('newsletter_consent', False)
        profile.save()

class UserProfileForm(forms.ModelForm):
    """
    Creates :form: from the :model:`bookings.UserProfile`
    Fields collected by the form are 'newsletter_consent'
    """
    newsletter_consent = forms.BooleanField(required=False)
    class Meta:
        model = UserProfile
        fields = ['newsletter_consent']

class WorkshopActivityForm(forms.ModelForm):
    """
    Creates :form: from the :model:`workshops.Workshop`
    Fields collected by the form are 'workshop activity'
    """
    class Meta:
        model = Workshop
        fields = ['activity']
    def __init__(self, *args, **kwargs):
        super(WorkshopActivityForm, self).__init__(*args, **kwargs)
        self.fields['activity'].queryset = WorkshopActivity.objects.filter(activity__publication_status=1).distinct("session_name")
    
class ReservationForm(forms.ModelForm):
    """
    Creates :form: from the :model:`bookings.Reservation`
    Fields collected by the form are 'workshop', 'tickets', 'has_dietary_requirements', 'additional_information' and 'consent_given`
    """
    class Meta: 
        model = Reservation
        fields = ['workshop', 'tickets', 'has_dietary_requirements', 'additional_information', 'consent_given']
    def __init__(self, *args, **kwargs):
        #ensures that workshops offered are only those which match the activity name previously selected by the customer
        #in the first stage of the booking process.
        workshop_name = kwargs.pop('workshop_name')
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields['workshop'].queryset = Workshop.objects.filter(activity = workshop_name, publication_status =1)
        self.fields['additional_information'].widget = forms.Textarea(attrs={'rows':4})

class FeedbackForm(forms.ModelForm):
    """
    Creates :form: from the :model:`bookings.Feedback`
    Fields collected by the form are 'feedback_rating', 'feedback_comment' and 'recommend'
    """
    feedback_rating = forms.IntegerField(widget=forms.RadioSelect(choices = RATING))

    class Meta:
        model = Feedback
        fields = ['feedback_rating', 'feedback_comment', 'recommend']

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields['feedback_comment'].widget = forms.Textarea(attrs={'rows':5})
