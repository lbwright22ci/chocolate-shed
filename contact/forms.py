from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    """
    Creates :form: from the :model:`cotact.Contact`
    Fields collected by the form are 'name', 'email' and 'messsage'
    """
    class Meta:
        model = Contact
        fields = ('name','email','comment',)