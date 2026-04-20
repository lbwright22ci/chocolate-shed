from django import forms
from .models import UserProfile

class CustomSignupForm(forms.Form):
    newsletter_consent = forms.BooleanField()
    def signup(self, request, user):

        user.save()
        profile = UserProfile(user=user)
        profile.newsletter_consent = self.cleaned_data.get('newsletter_consent', False)
        profile.save()