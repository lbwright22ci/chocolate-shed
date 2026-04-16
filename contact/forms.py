from django import forms
from crispy_forms.layout import Field, Fieldset
from .models import Contact

class ContactForm(forms.ModelForm):
    """
    Creates :form: from the :model:`cotact.Contact`
    Fields collected by the form are 'name', 'email' and 'messsage'
    """

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['comment'].widget = forms.Textarea(attrs={'rows':4})

    class Meta:
        model = Contact
        fields = ('name','email','comment',)