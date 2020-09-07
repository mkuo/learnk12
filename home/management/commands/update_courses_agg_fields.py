from sys import stdout

from django.core.management.base import BaseCommand
from django.db import connection
from django.db.models.signals import post_save, post_delete

from home.models import CourseReview


class Command(BaseCommand):
    help = 'Updates CoursePage and ProviderPage aggregate fields in case of mismatch due to race conditions'

    def handle(self, *args, **options):
        print("Checking for mismatched records:")
        self._handle_course_mismatches()
        self._handle_provider_mismatches()
        print("Check complete.")

    @staticmethod
    def _get_providers_with_mismatch():
        raw_sql = (
            'SELECT provider.page_ptr_id, provider.avg_score, AVG(review.score), provider.review_count, COUNT(review) '
            'FROM home_providerpage AS provider '
            'LEFT JOIN home_coursepage AS course ON provider.page_ptr_id = course.provider_id '
            'LEFT JOIN home_coursereview AS review ON review.course_page_id = course.page_ptr_id '
            'GROUP BY provider.page_ptr_id '
            'HAVING provider.avg_score != AVG(review.score) '
            'OR (provider.avg_score IS NULL AND AVG(review.score) IS NOT NULL) '
            'OR (provider.avg_score IS NOT NULL AND AVG(review.score) IS NULL) '
            'OR provider.review_count != COUNT(review)'
        )
        with connection.cursor() as cursor:
            cursor.execute(raw_sql)
            return cursor.fetchall()

    @staticmethod
    def _get_courses_with_mismatch():
        raw_sql = (
            'SELECT page_ptr_id, avg_score, AVG(review.score), review_count, COUNT(review) '
            'FROM home_coursepage AS course '
            'LEFT JOIN home_coursereview AS review ON review.course_page_id = course.page_ptr_id '
            'GROUP BY page_ptr_id '
            'HAVING avg_score != AVG(review.score) '
            'OR (avg_score IS NULL AND AVG(review.score) IS NOT NULL) '
            'OR (avg_score IS NOT NULL AND AVG(review.score) IS NULL) '
            'OR review_count != COUNT(review)'
        )
        with connection.cursor() as cursor:
            cursor.execute(raw_sql)
            return cursor.fetchall()

    def _handle_provider_mismatches(self):
        mismatched_providers = self._get_providers_with_mismatch()
        for provider_id, avg_score, avg_score_calc, review_count, review_count_calc in mismatched_providers:
            message = f'Mismatch found (provider_id: {provider_id}): '
            if avg_score != avg_score_calc:
                message += f'(avg_score: {avg_score}, calc: {avg_score_calc})'
            if review_count != review_count_calc:
                message += f'(review_count: {review_count}, calc: {review_count_calc})'
            stdout.write(message + '\n')
            course_review = CourseReview.objects.select_related('course_page'). \
                filter(course_page__provider_id=provider_id). \
                order_by('-date_modified').first()
            if course_review:
                post_save.send(CourseReview, instance=course_review)
            else:
                post_delete.send(CourseReview, instance=course_review)

    def _handle_course_mismatches(self):
        mismatched_courses = self._get_courses_with_mismatch()
        for course_id, avg_score, avg_score_calc, review_count, review_count_calc in mismatched_courses:
            message = f'Mismatch found (course_id: {course_id}): '
            if avg_score != avg_score_calc:
                message += f'(avg_score: {avg_score}, calc: {avg_score_calc})'
            if review_count != review_count_calc:
                message += f'(review_count: {review_count}, calc: {review_count_calc})'
            stdout.write(message + '\n')
            course_review = CourseReview.objects.filter(course_page_id=course_id). \
                order_by('-date_modified').first()
            if course_review:
                post_save.send(CourseReview, instance=course_review)
            else:
                post_delete.send(CourseReview, instance=course_review)
