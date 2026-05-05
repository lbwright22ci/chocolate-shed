from datetime import datetime, timedelta
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import Workshop, WorkshopActivity, WorkshopType

# Create your tests here.

class TestWorkshopViews(TestCase):

    def setUp(self):
        self.workshoptypechild = WorkshopType(target_audience = "CH",
                            workshop_duration= 90, workshop_price =30)
        self.workshoptypechild.save()
        self.workshoptypefamily = WorkshopType(target_audience = "FA",
                            workshop_duration= 90, workshop_price =30)
        self.workshoptypefamily.save()
        self.workshoptypeadult = WorkshopType(target_audience = "AD",
                            workshop_duration= 90, workshop_price =30)
        self.workshoptypeadult.save()
        self.workshopactivityopenchild = WorkshopActivity(session_name="open child workshop",
                                excerpt="a workshop", full_description="" \
                                "long description")
        self.workshopactivityopenchild.save()
        self.workshopactivityopenfamily = WorkshopActivity(session_name="open family workshop",
                                excerpt="a workshop", full_description="" \
                                "long description")
        self.workshopactivityopenfamily.save()
        self.workshopactivityopenadult = WorkshopActivity(session_name="open adult workshop",
                                excerpt="a workshop", full_description="" \
                                "long description")
        self.workshopactivityopenadult.save()
        self.workshopactivityclosed = WorkshopActivity(session_name="closed workshop",
                                excerpt="a workshop", full_description="" \
                                "long description")
        self.workshopactivityclosed.save()
        self.workshopactivitycanceled = WorkshopActivity(session_name="canceled workshop",
                                excerpt="a workshop", full_description="" \
                                "long description")
        self.workshopactivitycanceled.save()
        self.childworkshopopen = Workshop(category=self.workshoptypechild, activity=
                                 self.workshopactivityopenchild, slug="workshop-slug-open-child",
                                 location="on site", low_stock=False, 
                                 publication_status=1, event_date=timezone.now()+timedelta(days=30))
        self.childworkshopopen.save()
        self.familyworkshopopen = Workshop(category=self.workshoptypefamily, activity=
                                 self.workshopactivityopenfamily, slug="workshop-slug-open-family",
                                 location="on site", low_stock=False, 
                                 publication_status=1, event_date=timezone.now()+timedelta(days=31))
        self.familyworkshopopen.save()
        self.adultworkshopopen = Workshop(category=self.workshoptypeadult, activity=
                                 self.workshopactivityopenadult, slug="workshop-slug-open-adult",
                                 location="on site", low_stock=False, 
                                 publication_status=1, event_date=timezone.now()+timedelta(days=32))
        self.adultworkshopopen.save()
        self.childworkshopclosed = Workshop(category=self.workshoptypechild, activity=
                                 self.workshopactivityclosed, slug="workshop-slug-closed",
                                 location="on site", low_stock=False, 
                                 publication_status=3, event_date=timezone.now()+timedelta(days=1))
        self.childworkshopclosed.save()
        self.childworkshopcanceled = Workshop(category=self.workshoptypechild, activity=
                                 self.workshopactivitycanceled, slug="workshop-slug-canceled",
                                 location="on site", low_stock=False, 
                                 publication_status=2, event_date=timezone.now()+timedelta(days=20))
        self.childworkshopcanceled.save()

    def test_render_home_page_with_workshop_list(self):
        """ Verifies request to render home page content containing the
          list of workshops with open publication status """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"open child workshop", response.content)
        self.assertIn(b"open adult workshop", response.content)
        self.assertIn(b"open family workshop", response.content)
        self.assertNotIn(b"closed workshop", response.content)
        self.assertNotIn(b"canceled workshop", response.content)

    def test_render_childlist_page_with_only_childrens_workshops(self):
        """ Verifies request to render child list page content containing the
          list of workshops with open publication status """
        response = self.client.get(reverse('child_workshops'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"open child workshop", response.content)
        self.assertNotIn(b"open adult workshop", response.content)
        self.assertNotIn(b"open family workshop", response.content)
        self.assertNotIn(b"closed workshop", response.content)
        self.assertNotIn(b"canceled workshop", response.content)

    def test_render_adult_page_with_workshop_list(self):
        """ Verifies request to render adult list page content containing the
          list of workshops with open publication status """
        response = self.client.get(reverse('adult_workshops'))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"open child workshop", response.content)
        self.assertIn(b"open adult workshop", response.content)
        self.assertNotIn(b"open family workshop", response.content)
        self.assertNotIn(b"closed workshop", response.content)
        self.assertNotIn(b"canceled workshop", response.content)
    
    def test_render_familylist_page_with_only_childrens_workshops(self):
        """ Verifies request to render family list page content containing the
          list of workshops with open publication status """
        response = self.client.get(reverse('family_workshops'))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"open child workshop", response.content)
        self.assertNotIn(b"open adult workshop", response.content)
        self.assertIn(b"open family workshop", response.content)
        self.assertNotIn(b"closed workshop", response.content)
        self.assertNotIn(b"canceled workshop", response.content)
    
    def test_render_workshop_detail_page(self):
        """ Verifies request to render workshop detail page content containing
         full description, price, Faqs and feedback """
        response = self.client.get(reverse('workshop_detail', args=['workshop-slug-open-child']))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"long description", response.content)
        self.assertIn(b"FAQ", response.content)
        self.assertIn(b"Recent reviews", response.content)
        self.assertIn(b"30", response.content)
