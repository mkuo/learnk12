from decimal import Decimal

from django.core.validators import MaxValueValidator
from django.db import models, connection
from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver
from modelcluster.fields import ParentalKey

from home.submodels.course_detail_page import CourseDetailPage


class CourseReview(models.Model):
    course_detail_page = ParentalKey(
        'CourseDetailPage',
        on_delete=models.CASCADE,
        related_name='course_reviews'
    )

    # meta settings
    parent_page_type = ['CourseDetailPage']
    subpage_types = []

    # database fields
    score = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)])
    publish_date = models.DateField()
    subject = models.TextField()
    description = models.TextField()
    date_modified = models.DateTimeField(auto_now=True)

    class ReviewerType(models.TextChoices):
        STUDENT = 'student'
        PARENT = 'parent'
        TEACHER = 'teacher'
        BUSINESS = 'business'
    reviewer_type = models.CharField(choices=ReviewerType.choices, max_length=24)

    name = models.CharField(max_length=255)
    email = models.EmailField()
    is_anonymous = models.BooleanField()


@receiver(post_save, sender=CourseReview, dispatch_uid="update_course_avg_score")
def update_course_avg_score(sender, instance, **kwargs):
    raw_sql_select = (
        'SELECT page_ptr_id, AVG(review.score) '
        'FROM home_coursedetailpage AS course '
        'JOIN home_coursereview AS review ON review.course_detail_page_id = course.page_ptr_id '
        'WHERE course.page_ptr_id = {course_id} '
        'GROUP BY page_ptr_id'
    )
    # To minimize race conditions, this SQL update clause also checks that this CourserReview instance
    # matches the most recently modified home_coursereview for the related home_coursedetailpage
    # There still exists a race condition between the UPDATE and the SELECT subquery
    raw_sql_update = (
        'UPDATE home_coursedetailpage '
        'SET avg_score = {avg_score} '
        'WHERE page_ptr_id = {course_id} '
        'AND {review_id} = (SELECT id '
        'FROM home_coursereview '
        'WHERE course_detail_page_id = {course_id} '
        'ORDER BY date_modified DESC LIMIT 1)'
    )
    with connection.cursor() as cursor:
        cursor.execute(raw_sql_select.format(course_id=instance.course_detail_page_id))
        course_id, avg_score = cursor.fetchone()
        cursor.execute(raw_sql_update.format(
            avg_score=avg_score,
            course_id=course_id,
            review_id=instance.id
        ))
