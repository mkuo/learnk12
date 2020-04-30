from django.core.validators import MaxValueValidator
from django.db import models
from modelcluster.fields import ParentalKey

from home.submodels.course_detail_page import CourseDetailPage


class CourseReview(models.Model):
    course_detail_page = ParentalKey(
        CourseDetailPage,
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

    class ReviewerType(models.TextChoices):
        STUDENT = 'student'
        PARENT = 'parent'
        TEACHER = 'teacher'
        BUSINESS = 'business'
    reviewer_type = models.CharField(choices=ReviewerType.choices, max_length=24)

    name = models.CharField(max_length=255)
    email = models.EmailField()
    is_anonymous = models.BooleanField()
