from sys import stdout

from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.db.models.signals import post_save

from home.submodels.course_detail_page import CourseDetailPage
from home.submodels.course_review import update_course_avg_score, CourseReview


class Command(BaseCommand):
    help = 'Updates CourseDetailPage.avg_score in case of mismatch with aggregate of related CourseReview.score'

    @staticmethod
    def _get_courses_with_score_mismatch():
        raw_sql = (
            'SELECT page_ptr_id, avg_score, AVG(review.score)'
            'FROM home_coursedetailpage AS course '
            'LEFT JOIN home_coursereview AS review ON review.course_detail_page_id = course.page_ptr_id '
            'GROUP BY page_ptr_id '
            'HAVING avg_score != AVG(review.score) '
            'OR (avg_score IS NULL AND AVG(review.score) IS NOT NULL) '
            'OR (avg_score IS NOT NULL AND AVG(review.score) IS NULL)'
        )
        with connection.cursor() as cursor:
            cursor.execute(raw_sql)
            return cursor.fetchall()

    def handle(self, *args, **options):
        mismatched_courses = self._get_courses_with_score_mismatch()
        for course_id, avg_score, avg_score_calc in mismatched_courses:
            message = (
                f'Mismatch found: (course_id: {course_id}, '
                f'avg_score: {avg_score}, '
                f'avg_score_calc: {avg_score_calc})'
                '\n'
            )
            stdout.write(message)
            course_review = CourseReview.objects.filter(course_detail_page_id=course_id).\
                order_by('-date_modified').first()
            if course_review:
                post_save.send(CourseReview, instance=course_review)
            else:
                CourseDetailPage.objects.filter(page_ptr_id=course_id).update(avg_score=None)
