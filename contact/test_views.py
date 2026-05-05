from django.test import TestCase, Client
from django.urls import reverse
from .forms import ContactForm
from .models import Contact

# Create your tests here.


class TestContactViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_render_contact_page_with_contact_form(self):
        """ Verifies request to render Contact page content containing the
          contact form """
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Get in touch!", response.content)
        self.assertIn(b"No issue is too big or small", response.content)
        self.assertIsInstance(response.context['contact_form'], ContactForm)

    def test_successful_contact_us_submission(self):
        """Test for posting a contact us request on the contact page"""
        post_data = {
            'name': 'name', 'email': 'test@test.com',
            'comment': 'do you have workshops on Christmas day?'
        }
        response = self.client.post(reverse(
            'contact'), post_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'Thank you for contacting The Chocolate Shed.',
            response.content
        )
