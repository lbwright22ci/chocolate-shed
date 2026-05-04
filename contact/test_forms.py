from django.test import TestCase
from .forms import ContactForm

# Create your tests here.

class TestContactForm(TestCase):

    def test_form_is_valid(self):
        """ Test that form is valid when all fields are completed """
        form = ContactForm({
            'name': 'name',
            'email': 'test@test.com',
            'comment': 'Hello!'
        })
        self.assertTrue(form.is_valid(), msg='Form is not valid')
    def test_form_is_invalid_if_name_is_blank(self):
        """ Test that form is declared invalid if name is not completed """
        form = ContactForm({
            'name': '',
            'email': 'test@test.com',
            'comment': 'Hello!'
        })
        self.assertFalse(form.is_valid(), msg='Form is valid when name is blank')
    def test_form_is_invalid_if_email_is_blank(self):
        """ Test that form is declared invalid if email is not completed"""
        form = ContactForm({
            'name': 'name',
            'email': '',
            'comment': 'Hello!'
        })
        self.assertFalse(form.is_valid(), msg='Form is valid when email is blank')
    def test_form_is_invalid_if_comment_is_blank(self):
        """ Test that form is declared invalid if comment is not completed"""
        form = ContactForm({
            'name': 'name',
            'email': 'test@test.com',
            'comment': ''
        })
        self.assertFalse(form.is_valid(), msg='Form is valid when comment is blank')

