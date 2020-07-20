from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, connection
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from modelcluster.fields import ParentalKey

from user_auth.models import User


class TutorReview(models.Model):
    tutor_page = ParentalKey(
        'TutorPage',
        on_delete=models.CASCADE,
        related_name='tutor_reviews'
    )

    # meta settings
    parent_page_type = ['TutorPage']
    subpage_types = []

    # database fields
    score = models.PositiveSmallIntegerField(db_index=True, validators=[
        MinValueValidator(1), MaxValueValidator(5)
    ])
    publish_date = models.DateTimeField(db_index=True, auto_now_add=True)
    subject = models.TextField(db_index=True)
    description = models.TextField(db_index=True)
    date_modified = models.DateTimeField(db_index=True, auto_now=True)

    class ReviewerType(models.TextChoices):
        STUDENT = 'student'
        PARENT = 'parent'
        TEACHER = 'teacher'

    reviewer_type = models.CharField(choices=ReviewerType.choices, max_length=24)

    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(db_index=True, null=True, blank=True)
    is_anonymous = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


@receiver(post_save, sender=TutorReview, dispatch_uid="post_save_tutor_agg_fields")
def post_save_tutor_agg_fields(sender, instance, **kwargs):
    raw_sql_select = (
        'SELECT page_ptr_id, AVG(review.score), COUNT(*) '
        'FROM home_tutorpage AS tutor '
        'JOIN home_tutorreview AS review ON review.tutor_page_id = tutor.page_ptr_id '
        'WHERE tutor.page_ptr_id = {tutor_id} '
        'GROUP BY page_ptr_id'
    )
    raw_sql_update = (
        'UPDATE home_tutorpage '
        'SET avg_score = {avg_score}, review_count = {review_count} '
        'WHERE page_ptr_id = {tutor_id} '
        'AND {review_id} = (SELECT id '
        'FROM home_tutorreview '
        'WHERE tutor_page_id = {tutor_id} '
        'ORDER BY date_modified DESC LIMIT 1)'
    )
    with connection.cursor() as cursor:
        cursor.execute(raw_sql_select.format(tutor_id=instance.tutor_page_id))
        tutor_id, avg_score, review_count = cursor.fetchone()
        cursor.execute(raw_sql_update.format(
            avg_score=avg_score,
            review_count=review_count,
            tutor_id=tutor_id,
            review_id=instance.id
        ))


@receiver(post_delete, sender=TutorReview, dispatch_uid="post_delete_tutor_agg_fields")
def post_delete_tutor_agg_fields(sender, instance, **kwargs):
    tutor_review = TutorReview.objects.filter(tutor_page_id=instance.tutor_page_id). \
        order_by('-date_modified').first()
    if tutor_review:
        post_save_tutor_agg_fields(sender, tutor_review, **kwargs)
    else:
        raw_sql_update = (
            'UPDATE home_tutorpage '
            'SET avg_score = null, review_count = 0 '
            'WHERE page_ptr_id = {tutor_id} '
            'AND (SELECT id '
            'FROM home_tutorreview '
            'WHERE tutor_page_id = {tutor_id} '
            'ORDER BY date_modified DESC LIMIT 1) IS NULL'
        )
        with connection.cursor() as cursor:
            cursor.execute(raw_sql_update.format(tutor_id=instance.tutor_page_id))
