from sys import stdout

from django.core.management.base import BaseCommand
from django.db import connection
from django.db.models.signals import post_save, post_delete

from home.models import TutorReview


class Command(BaseCommand):
    help = 'Updates TutorPage aggregate fields in case of mismatch due to race conditions'

    @staticmethod
    def _get_tutors_with_mismatch():
        raw_sql = (
            'SELECT page_ptr_id, avg_score, AVG(review.score), review_count, COUNT(review) '
            'FROM home_tutorpage AS tutor '
            'LEFT JOIN home_tutorreview AS review ON review.tutor_page_id = tutor.page_ptr_id '
            'GROUP BY page_ptr_id '
            'HAVING avg_score != AVG(review.score) '
            'OR (avg_score IS NULL AND AVG(review.score) IS NOT NULL) '
            'OR (avg_score IS NOT NULL AND AVG(review.score) IS NULL) '
            'OR review_count != COUNT(review)'
        )
        with connection.cursor() as cursor:
            cursor.execute(raw_sql)
            return cursor.fetchall()

    def handle(self, *args, **options):
        print("Checking for mismatched tutors:")
        mismatched_tutors = self._get_tutors_with_mismatch()
        for tutor_id, avg_score, avg_score_calc, review_count, review_count_calc in mismatched_tutors:
            message = f'Mismatch found (tutor_id: {tutor_id}): '
            if avg_score != avg_score_calc:
                message += f'(avg_score: {avg_score}, calc: {avg_score_calc})'
            if review_count != review_count_calc:
                message += f'(review_count: {review_count}, calc: {review_count_calc})'
            stdout.write(message + '\n')
            tutor_review = TutorReview.objects.filter(tutor_page_id=tutor_id). \
                order_by('-date_modified').first()
            if tutor_review:
                post_save.send(TutorReview, instance=tutor_review)
            else:
                post_delete.send(TutorReview, instance=tutor_review)
        print("Check complete.")
