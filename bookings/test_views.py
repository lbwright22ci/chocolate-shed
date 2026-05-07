from datetime import datetime, timedelta
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from workshops.models import Workshop, WorkshopActivity, WorkshopType
from .forms import UserProfileForm, ReservationForm, FeedbackForm
from .models import Reservation, Feedback, UserProfile

# Create your tests here.


class TestBookingsViews(TestCase):
    def setUp(self):
        # create a user so that can simulate logged-in user views
        self.user = User.objects.create_user(username='username',
                                             email='test@user.com',
                                             password='password123',
                                             first_name='First name',
                                             last_name='Last name')
        self.superuser = User.objects.create_user(username='adminstaff',
                                                  email='test@admin.com',
                                                  first_name='admin',
                                                  last_name='staff',
                                                  is_staff=True,
                                                  password='passwordabc')
        self.userprofile = UserProfile(user=self.user,
                                       newsletter_consent=True,
                                       staff_status=True)
        self.userprofile.save()
        self.userprofileadmin = UserProfile(user=self.superuser,
                                            newsletter_consent=True,
                                            staff_status=True)
        self.userprofileadmin.save()
        self.workshoptype = WorkshopType(target_audience="CH",
                                         workshop_duration=90,
                                         workshop_price=30)
        self.workshoptype.save()
        self.workshoptypefamily = WorkshopType(target_audience="FA",
                                               workshop_duration=90,
                                               workshop_price=30)
        self.workshoptypefamily.save()
        self.workshopactivity = WorkshopActivity(session_name="open"
                                                 " child workshop",
                                                 excerpt="a workshop",
                                                 full_description=""
                                                 "long description")
        self.workshopactivity.save()
        self.workshopactivityfamily = WorkshopActivity(session_name="open"
                                                       " family workshop",
                                                       excerpt="a workshop",
                                                       full_description=""
                                                       "long description")
        self.workshopactivityfamily.save()
        self.workshopactivityclosed = WorkshopActivity(session_name="closed"
                                                       " child workshop",
                                                       excerpt="a workshop",
                                                       full_description=""
                                                       "long description")
        self.workshopactivityclosed.save()
        self.workshopopen = Workshop(category=self.workshoptype,
                                     activity=self.workshopactivity,
                                     slug="workshop-slug-open",
                                     location="on site", low_stock=False,
                                     tickets_sold=2,
                                     publication_status=1,
                                     event_date=timezone.now() +
                                     timedelta(days=30))
        self.workshopopen.save()
        self.workshopopenfamily = Workshop(category=self.workshoptypefamily,
                                           activity=self.workshopactivityfamily,
                                           slug="workshop-slug-open-family",
                                           location="on site", low_stock=False,
                                           tickets_sold=0,
                                           publication_status=1,
                                           event_date=timezone.now() +
                                           timedelta(days=31))
        self.workshopopenfamily.save()
        self.workshopclosed = Workshop(category=self.workshoptype,
                                       activity=self.workshopactivityclosed,
                                       slug="workshop-slug-closed",
                                       location="on site", low_stock=False,
                                       publication_status=3,
                                       event_date=timezone.now() -
                                       timedelta(days=20))
        self.workshopclosed.save()
        self.pendingbooking = Reservation(workshop=self.workshopopen,
                                          customer=self.user,
                                          tickets=2, consent_given=True,
                                          has_dietary_requirements=True,
                                          additional_information='reservation'
                                          ' pending shows')
        self.pendingbooking.save()
        self.oldbooking = Reservation(workshop=self.workshopclosed,
                                      customer=self.user,
                                      tickets=3, consent_given=True)
        self.oldbooking.save()
        # self.review = Feedback(booking=self.oldbooking, feedback_rating = 0,
        #                        submitted= False)
        # self.review.save()

    def test_settingsaccountpage_renders_correctly(self):
        """ tests that logged in user can view settings account page"""
        self.client.login(email='test@user.com', password='password123')
        response = self.client.get(reverse('my_account'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"test@user.com", response.content)
        self.assertIn(b"You are subscribed to our mailing list",
                      response.content)

    def test_newsletter_update_page_renders_correctly(self):
        """ tests that logged in user can view page"""
        self.client.login(email='test@user.com', password='password123')
        response = self.client.get(reverse('update_mailing'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Update mailing list preferences", response.content)
        self.assertIsInstance(response.context['form'], UserProfileForm)

    def test_newsletter_status_updated_correctly(self):
        """ Tests that logged in user can update their mailing
          list preferences"""
        self.client.login(
            email="test@user.com", password="password123")
        post_data = {
            'newsletter_consent': False
        }
        response = self.client.post(reverse(
            'update_mailing'), post_data)
        self.assertEqual(response.status_code, 302)
        self.userprofile.refresh_from_db()
        self.assertEqual(self.userprofile.newsletter_consent, False)

    def test_stage_two_booking_renders_correctly(self):
        """ tests that logged in user can view stage two of booking form"""
        self.client.login(email='test@user.com', password='password123')
        response = self.client.get(reverse('submitbooking'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Number of tickets to reserve", response.content)
        self.assertIsInstance(
            response.context['booking_form'], ReservationForm)

    def test_update_booking_renders_correctly(self):
        """ tests that logged in user can update a pending booking"""
        self.client.login(email='test@user.com', password='password123')
        response = self.client.get(
            reverse('update_booking', args=[self.pendingbooking.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Update booking details", response.content)
        self.assertIsInstance(response.context['form'], ReservationForm)

    def test_update_booking_posts_data_correctly(self):
        """ Tests that logged in user can post data to update a booking
        booking form if everything is complete"""
        self.client.login(
            email="test@user.com", password="password123")
        post_data = {
            'workshop': self.pendingbooking.workshop.pk,
            'tickets': 6,
            'has_dietary_requirements': True,
            'additional_information': 'updated',
            'consent_given': True
        }
        response = self.client.post(
            reverse('update_booking', args=[self.pendingbooking.id]),
            post_data)
        self.assertEqual(response.status_code, 302)
        self.pendingbooking.refresh_from_db()
        self.assertEqual(self.pendingbooking.tickets, 6)

    def test_stage_two_booking_posts_data_correctly(self):
        """ Tests that logged in user can post data
          through the second stage of the
        booking form if everything is complete"""
        self.client.login(
            email="test@user.com", password="password123")
        session = self.client.session
        session['workshop_name'] = self.workshopactivity.pk
        session.save()
        post_data = {
            'workshop': self.workshopopen.pk,
            'tickets': 2,
            'has_dietary_requirements': True,
            'additional_information': 'test that this booking exists',
            'consent_given': True
        }
        response = self.client.post(reverse(
            'submitbooking'), post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Reservation.objects.count(), 3)

    def test_stage_two_booking_posts_invalid_too_many_tickets(self):
        """ Tests that logged in user cannot
          post data through the second stage of the
        booking form if too many tickets"""
        self.client.login(
            email="test@user.com", password="password123")
        session = self.client.session
        session['workshop_name'] = self.workshopactivity.pk
        session.save()
        post_data = {
            'workshop': self.workshopopen.pk,
            'tickets': 200,
            'has_dietary_requirements': True,
            'additional_information': 'test that this booking exists',
            'consent_given': True
        }
        response = self.client.post(reverse(
            'submitbooking'), post_data)
        self.assertNotEqual(response.status_code, 302)
        self.assertEqual(Reservation.objects.count(), 2)

    def test_stage_two_booking_invalid_one_ticket_family_session(self):
        """ Tests that logged in user cannot post data through
          the second stage of the
        booking form if only one ticket reserved for a
          family session"""
        self.client.login(
            email="test@user.com", password="password123")
        session = self.client.session
        session['workshop_name'] = self.workshopactivityfamily.pk
        session.save()
        post_data = {
            'workshop': self.workshopopenfamily.pk,
            'tickets': 1,
            'has_dietary_requirements': True,
            'additional_information': 'test that this booking exists',
            'consent_given': True
        }
        response = self.client.post(reverse(
            'submitbooking'), post_data)
        self.assertNotEqual(response.status_code, 302)
        self.assertEqual(Reservation.objects.count(), 2)

    def test_delete_booking_renders_correctly(self):
        """ tests that logged in user can delete a pending booking"""
        self.client.login(email='test@user.com', password='password123')
        response = self.client.get(
            reverse('delete_booking', args=[self.pendingbooking.id]))
        self.assertEqual(response.status_code, 302)

    def test_delete_booking_posts_data_correctly(self):
        """ Tests that logged in user can post data to delete a booking
        if everything is complete"""
        self.client.login(
            email="test@user.com", password="password123")
        response = self.client.post(
            reverse('delete_booking', args=[self.pendingbooking.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Reservation.objects.count(), 1)

    def test_my_bookingslist_renders_correctly(self):
        """ Tests that booking list details open reservations but not
          closed ones """
        self.client.login(email="test@user.com", password="password123")
        response = self.client.get(reverse('my_bookingsList'))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"closed child workshop", response.content)
        self.assertIn(b"open child workshop", response.content)
        self.assertIn(b"My Workshops", response.content)

    def test_my_feedbacklist_renders_correctly(self):
        """ Tests that feedback list details closed reservations but
          not open ones """
        self.client.login(email="test@user.com", password="password123")
        response = self.client.get(reverse('feedback_page'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"closed child workshop", response.content)
        self.assertNotIn(b"open child workshop", response.content)
        self.assertIn(b"Leave Feedback!", response.content)

    def test_staff_page_renders_correctly(self):
        """ Tests that staff page lists all open workshops and reservations
         and that if not user.staff then can't see links to django admin """
        self.client.login(email="test@user.com", password="password123")
        response = self.client.get(reverse('staff_page'))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"closed child workshop", response.content)
        self.assertIn(b"open child workshop", response.content)
        self.assertIn(b"open family workshop", response.content)
        self.assertIn(b'reservation pending shows', response.content)
        self.assertNotIn(b'Quick access links', response.content)

    def test_staff_page_renders_correctly_for_admin(self):
        """ Tests that staff page lists all open workshops and reservations
         and that if user.staff then can see links to django admin """
        self.client.login(email="test@admin.com", password="passwordabc")
        response = self.client.get(reverse('staff_page'))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"closed child workshop", response.content)
        self.assertIn(b"open child workshop", response.content)
        self.assertIn(b"open family workshop", response.content)
        self.assertIn(b'reservation pending shows', response.content)
        self.assertIn(b'Quick access links', response.content)

    def test_leave_feedback_page_specific_session_renders_correctly(self):
        """ Tests that user can update or add feedback after a workshop
         plus that feedback is given with approved status False """
        self.client.login(email="test@user.com", password="password123")
        review_id = Feedback.objects.get(booking=self.oldbooking)
        response = self.client.get(
            reverse('feedback_form', args=[review_id.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Leaving feedback for", response.content)
        self.assertIsInstance(response.context['form'], FeedbackForm)

    def test_update_feedback_posts_data_correctly(self):
        """ Tests that logged in user can post data to update a booking
        booking form if everything is complete"""
        self.client.login(
            email="test@user.com", password="password123")
        post_data = {
            'feedback_rating': 5,
            'feedback_comment': 'great',
            'recommend': True
        }
        review_id = Feedback.objects.get(booking=self.oldbooking)
        response = self.client.post(
            reverse('feedback_form', args=[review_id.id]), post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Feedback.objects.get(
            pk=review_id.id).feedback_rating, 5)
        self.assertNotEqual(Feedback.objects.get(
            pk=review_id.id).approved, True)
