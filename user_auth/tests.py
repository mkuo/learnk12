from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from home.models import CourseReview, CoursePage, ProviderPage, SiteFeedback
from user_auth.models import User


class SignUpPageTests(TestCase):

    def test_success_signup(self):
        self.client.post(reverse('signup'),
                         data={'first_name': 'fjohndoe',
                               'last_name': 'ljohndoe',
                               'email': 'john@examples.org',
                               'password1': 'VeryHardPassword',
                               'password2': 'VeryHardPassword'})
        self.assertEqual(User.objects.filter(email='john@examples.org').count(), 1)

    def test_signup_password_twice_form_error(self):
        resp = self.client.post(reverse('signup'),
                                data={'first_name': 'fjohndoe',
                                      'last_name': 'ljohndoe',
                                      'email': 'john@examples.org',
                                      'password1': 'johndoe',
                                      'password2': 'janedoe'})
        self.assertFormError(resp, 'form', 'password2', 'The two password fields didn’t match.')


    def test_low_password_signup(self):
        self.client.post(reverse('signup'),
                         data={'first_name': 'fjohndoe',
                               'last_name': 'ljohndoe',
                               'email': 'john@examples.org',
                               'password1': 'fjohndoe',
                               'password2': 'fjohndoe'})
        self.assertEqual(User.objects.filter(email='john@examples.org').count(), 0)


class LoginTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(username='testlogin@mail.com', email='testlogin@mail.com',
                                                    is_active=True)
        user.set_password('VeryHardPassword')
        user.save()

        EmailAddress.objects.create(user=user, email="testlogin@mail.com",
                                    primary=True, verified=True)

    def test_login_success(self):
        """Test for success login and access to account profile"""
        self.client.post(reverse('account_login'), {'login': 'testlogin@mail.com', 'password': 'VeryHardPassword'})
        resp = self.client.get(reverse('profile'))
        self.assertEqual(resp.status_code, 200)

    def test_login_failed_password(self):
        """Test for failed login and not access to account profile"""
        self.client.post(reverse('account_login'), {'login': 'testlogin@mail.com', 'password': 'failedpassword'})
        resp = self.client.get(reverse('profile'))
        self.assertEqual(resp.status_code, 302)

    def test_login_invalid_login(self):
        """Test for failed login and not access to account profile"""
        self.client.post(reverse('account_login'), {'login': 'invalidlogin@mail.com', 'password': 'VeryHardPassword'})
        resp = self.client.get(reverse('profile'))
        self.assertEqual(resp.status_code, 302)


class AccountTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(username='testlogin@mail.com', email='testlogin@mail.com',
                                                    is_active=True)
        user.set_password('VeryHardPassword')
        user.save()

        EmailAddress.objects.create(user=user, email="testlogin@mail.com",
                                    primary=True, verified=True)

    def test_success_password_reset(self):
        self.client.login(username='testlogin@mail.com', password='VeryHardPassword')
        self.client.post(reverse('account_change_password'), {
            'oldpassword': 'VeryHardPassword', 'password1': 'newpass123',
            'password2': 'newpass123'})
        response = self.client.login(username='testlogin@mail.com', password='newpass123')
        self.assertEqual(response, True)

    def test_failed_password_reset(self):
        self.client.login(username='testlogin@mail.com', password='VeryHardPassword')
        self.client.post(reverse('account_change_password'), {
            'oldpassword': 'invalid', 'password1': 'newpass123',
            'password2': 'newpass123'})
        response = self.client.login(username='testlogin@mail.com', password='newpass123')
        self.assertEqual(response, False)


class ChangeReviews(TestCase):
    def setUp(self):
        provider_page = ProviderPage.objects.create(description='Test Description', title='Some Title', path='Test',
                                                    depth='1')
        course = CoursePage.objects.create(provider=provider_page, title='Some Title', path='Test_course', depth='1')
        self.review = CourseReview.objects.create(course_page=course, name='test', email='test@mail.com',
                                                  subject='Some Text',
                                                  description='Some Description', score=3, reviewer_type='student')

    def test_change_reviews(self):
        self.client.post(reverse('signup'),
                         data={'first_name': 'fjohndoe',
                               'last_name': 'ljohndoe',
                               'email': 'test@mail.com',
                               'password1': 'VeryHardPassword',
                               'password2': 'VeryHardPassword'})
        review = CourseReview.objects.filter(subject='Some Text').first()
        new_user = User.objects.filter(email='test@mail.com').first()
        self.assertEqual(new_user, review.user)


class ChangeSiteFeedback(TestCase):
    def setUp(self):
        self.site_feedback = SiteFeedback.objects.create(subject='Some subject', description='Some description',
                                                         name='test',
                                                         email='test@mail.com')

    def test_change_feedback(self):
        self.client.post(reverse('signup'),
                         data={'first_name': 'fjohndoe',
                               'last_name': 'ljohndoe',
                               'email': 'test@mail.com',
                               'password1': 'VeryHardPassword',
                               'password2': 'VeryHardPassword'})
        site_feedback = SiteFeedback.objects.filter(subject='Some subject').first()
        new_user = User.objects.filter(email='test@mail.com').first()
        self.assertEqual(new_user, site_feedback.user)
