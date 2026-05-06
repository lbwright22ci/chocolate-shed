from datetime import datetime, timedelta
from django.test import TestCase
from django.utils import timezone
from workshops.models import WorkshopType, Workshop, WorkshopActivity
from .forms import UserProfileForm, ReservationForm, FeedbackForm

# Create your tests here.


class TestUserProfileForm(TestCase):

    def test_form_is_valid_when_consent_to_mailing_list_given(self):
        """ Test that form is valid when newsletter consent is given
          completed """
        form = UserProfileForm({
            'newsletter_consent': True
        })
        self.assertTrue(form.is_valid(), msg='Form is not valid')

    def test_form_is_valid_when_consent_to_mailing_list_not_given(self):
        """ Test that form is declared valid if consent not given to 
         be on the mailing list """
        form = UserProfileForm({
            'newsletter_consent': False
        })
        self.assertTrue(
            form.is_valid(), msg='Form is invalid when mailing list consent not given')


class TestReservationForm(TestCase):

    def test_form_is_valid_when_all_fields_selected(self):
        """ Test that form is valid when all fields completed """
        WorkshopActivity.objects.create(session_name="adult workshop1", excerpt="a workshop", full_description=""
                                        "long description")
        act_pk = WorkshopActivity.objects.get(session_name="adult workshop1")
        WorkshopType.objects.create(
            target_audience="AD", workshop_duration=90, workshop_price=30)
        typ_pk = WorkshopType.objects.get(workshop_price=30)
        Workshop.objects.create(category=typ_pk, activity=act_pk, slug="workshop-slug",
                                location="on site", low_stock=False,
                                publication_status=1,
                                event_date=timezone.now()+timedelta(days=30))
        wkp_pk = Workshop.objects.get(slug="workshop-slug").pk
        form = ReservationForm({
            'workshop': wkp_pk,
            'tickets': 1,
            'has_dietary_requirements': True,
            'additional_information': 'extra info',
            'consent_given': True
            }, workshop_name = act_pk.pk)
        self.assertTrue(form.is_valid(), msg='Form is not valid')

    def test_form_not_valid_with_no_tickets(self):
        """ Test that form is not valid when all no tickets added """
        WorkshopActivity.objects.create(session_name="adult workshop1", excerpt="a workshop", full_description=""
                                        "long description")
        act_pk = WorkshopActivity.objects.get(session_name="adult workshop1")
        WorkshopType.objects.create(
            target_audience="AD", workshop_duration=90, workshop_price=30)
        typ_pk = WorkshopType.objects.get(workshop_price=30)
        Workshop.objects.create(category=typ_pk, activity=act_pk, slug="workshop-slug",
                                location="on site", low_stock=False,
                                publication_status=1,
                                event_date=timezone.now()+timedelta(days=30))
        wkp_pk = Workshop.objects.get(slug="workshop-slug").pk
        form = ReservationForm({
            'workshop': wkp_pk,
            'tickets': '',
            'has_dietary_requirements': True,
            'additional_information': 'extra info',
            'consent_given': True
            }, workshop_name = act_pk.pk)
        self.assertFalse(form.is_valid(), msg='Form is valid even if no tickets selected')
    
    def test_form_is_valid_has_dietary_requirements_false(self):
        """ Test that form is valid when no dietary requirements declared. """
        WorkshopActivity.objects.create(session_name="family workshop", excerpt="a workshop", full_description=""
                                        "long description")
        act_pk = WorkshopActivity.objects.get(session_name="family workshop")
        WorkshopType.objects.create(
            target_audience="FA", workshop_duration=90, workshop_price=30)
        typ_pk = WorkshopType.objects.get(workshop_price=30)
        Workshop.objects.create(category=typ_pk, activity=act_pk, slug="workshop-slug",
                                location="on site", low_stock=False,
                                publication_status=1,
                                event_date=timezone.now()+timedelta(days=30))
        wkp_pk = Workshop.objects.get(slug="workshop-slug").pk
        form = ReservationForm({
            'workshop': wkp_pk,
            'tickets': 1,
            'has_dietary_requirements': False,
            'additional_information': 'extra info',
            'consent_given': True
            }, workshop_name = act_pk.pk)
        self.assertTrue(form.is_valid(), msg='Form is invalid if no dietary requirements selected')

    def test_form_is_valid_consent_given_is_false(self):
        """ Test that form is valid when consent given field is false. """
        WorkshopActivity.objects.create(session_name="family workshop", excerpt="a workshop", full_description=""
                                        "long description")
        act_pk = WorkshopActivity.objects.get(session_name="family workshop")
        WorkshopType.objects.create(
            target_audience="FA", workshop_duration=90, workshop_price=30)
        typ_pk = WorkshopType.objects.get(workshop_price=30)
        Workshop.objects.create(category=typ_pk, activity=act_pk, slug="workshop-slug",
                                location="on site", low_stock=False,
                                publication_status=1,
                                event_date=timezone.now()+timedelta(days=30))
        wkp_pk = Workshop.objects.get(slug="workshop-slug").pk
        form = ReservationForm({
            'workshop': wkp_pk,
            'tickets': 1,
            'has_dietary_requirements': True,
            'additional_information': 'extra info',
            'consent_given': False
            }, workshop_name = act_pk.pk)
        self.assertTrue(form.is_valid(), msg='Form is invalid if consent given is false')

    def test_form_is_valid_additional_info_blank(self):
        """ Test that form is valid when additional info is blank. """
        WorkshopActivity.objects.create(session_name="family workshop", excerpt="a workshop", full_description=""
                                        "long description")
        act_pk = WorkshopActivity.objects.get(session_name="family workshop")
        WorkshopType.objects.create(
            target_audience="FA", workshop_duration=90, workshop_price=30)
        typ_pk = WorkshopType.objects.get(workshop_price=30)
        Workshop.objects.create(category=typ_pk, activity=act_pk, slug="workshop-slug",
                                location="on site", low_stock=False,
                                publication_status=1,
                                event_date=timezone.now()+timedelta(days=30))
        wkp_pk = Workshop.objects.get(slug="workshop-slug").pk
        form = ReservationForm({
            'workshop': wkp_pk,
            'tickets': 1,
            'has_dietary_requirements': True,
            'additional_information': '',
            'consent_given': False
            }, workshop_name = act_pk.pk)
        self.assertTrue(form.is_valid(), msg='Form is invalid if additional info is left blank')

    def test_form_is_invalid_no_workshop_selected(self):
        """ Test that form is invalid if no workshop is selected """
        WorkshopActivity.objects.create(session_name="family workshop", excerpt="a workshop", full_description=""
                                        "long description")
        act_pk = WorkshopActivity.objects.get(session_name="family workshop")
        WorkshopType.objects.create(
            target_audience="FA", workshop_duration=90, workshop_price=30)
        typ_pk = WorkshopType.objects.get(workshop_price=30)
        Workshop.objects.create(category=typ_pk, activity=act_pk, slug="workshop-slug",
                                location="on site", low_stock=False,
                                publication_status=1,
                                event_date=timezone.now()+timedelta(days=30))
        wkp_pk = Workshop.objects.get(slug="workshop-slug").pk
        form = ReservationForm({
            'workshop': '',
            'tickets': 1,
            'has_dietary_requirements': True,
            'additional_information': 'extra info',
            'consent_given': True
            }, workshop_name = act_pk.pk)
        self.assertFalse(form.is_valid(), msg='Form is valid if no workshop selected')

class TestFeedbackForm(TestCase):

    def test_form_is_valid_when_all_fields_selected(self):
        """ Test that form is valid when all fields completed """
        form = FeedbackForm({
            'feedback_rating':1,
            'feedback_comment':'comment',
            'recommend': True
            })
        self.assertTrue(form.is_valid(), msg='Form is not valid')
    def test_form_is_valid_when_comment_is_blank(self):
        """ Test that form is valid when feedback comment is blank """
        form = FeedbackForm({
            'feedback_rating':1,
            'feedback_comment':'',
            'recommend': True
            })
        self.assertTrue(form.is_valid(), msg='Form is not valid')
    def test_form_is_invalid_when_feedback_rating_is_blank(self):
        """ Test that form is valid when feedback comment is blank """
        form = FeedbackForm({
            'feedback_rating':'',
            'feedback_comment':'comment',
            'recommend': True
            })
        self.assertFalse(form.is_valid(), msg='Form is valid when feedback rating is blank')
    def test_form_is_valid_when_recommend_is_false(self):
        """ Test that form is valid when feedback comment is blank """
        form = FeedbackForm({
            'feedback_rating':1,
            'feedback_comment':'comment',
            'recommend': False
            })
        self.assertTrue(form.is_valid(), msg='Form is not valid')