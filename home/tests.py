from django.contrib.auth import get_user_model
from django.test import TestCase

from home.models import ProviderPage, CoursePage, CourseReview, TutorReview, TutorPage


class UpdateTutors(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(username='testlogin@mail.com', email='testlogin@mail.com',
                                                    is_active=True)
        user.set_password('VeryHardPassword')
        user.save()

        tutor = TutorPage.objects.create(user=user, title='Some Title', path='path', depth='1', course_subjects='Math',
                                         is_accepting_students=True, hourly_rate=25, timezone='UTC−12:00',
                                         description='Some description', avg_score=40)
        review = TutorReview.objects.create(tutor_page=tutor, name='test', email='test@mail.com', subject='Some Text',
                                            description='Some Description', score=3, reviewer_type='student',
                                            is_anonymous=False)

    def test_mismath_tutors(self):
        tutor = TutorPage.objects.filter(title='Some Title').first()
        review = TutorReview.objects.filter(tutor_page_id=tutor.id).first()
        tutor_score = tutor.avg_score
        review_score = float(review.score)
        self.assertEqual(tutor_score, review_score)

        # print(tutor_score, review_score)


class UpdateCourses(TestCase):
    def setUp(self):
        provider_page = ProviderPage.objects.create(description='Test Description', title='Some Title', path='Test',
                                                    depth='1')
        course = CoursePage.objects.create(provider=provider_page, title='Some Title', path='Test_course', depth='1')
        review = CourseReview.objects.create(course_page=course, name='test', email='test@mail.com',
                                             subject='Some Text',
                                             description='Some Description', score=3, reviewer_type='student')

    def test_mismath_tutors(self):
        course = CoursePage.objects.filter(title='Some Title').first()
        review = CourseReview.objects.filter(course_page_id=course.id).first()
        course_score = course.avg_score
        review_score = float(review.score)
        self.assertEqual(course_score, review_score)
