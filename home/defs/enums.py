from django.db import models


class CourseDifficulty(models.IntegerChoices):
    EASY = 0
    MEDIUM = 1
    HARD = 2


class CourseSubject(models.TextChoices):
    COMPUTER_SCIENCE = 'Computer Science'
    MATH = 'Math'
