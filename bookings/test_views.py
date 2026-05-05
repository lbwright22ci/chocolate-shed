from datetime import datetime, timedelta
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from workshops.models import Workshop, WorkshopActivity, WorkshopType
from models import Reservation, Feedback

# Create your tests here.

class TestBookingViews(TestCase):

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
                                 publication_status=3, event_date=timezone.now()-timedelta(days=10))
        self.childworkshopclosed.save()
        self.childworkshopcanceled = Workshop(category=self.workshoptypechild, activity=
                                 self.workshopactivitycanceled, slug="workshop-slug-canceled",
                                 location="on site", low_stock=False, 
                                 publication_status=2, event_date=timezone.now()+timedelta(days=20))
        self.childworkshopcanceled.save()
        # for testing Feedback from past workshop is displayed on the workshop detail
        # page
        self.customer = User.objects.create_user(email="test@test.com", password="myPassword", username="myUsername")
        self.customer.save()
        self.customer2 = User.objects.create_user(email="test1@test.com", password="secondpassword", username="anotherperson")
        self.customer2.save()
# Create your tests here.
