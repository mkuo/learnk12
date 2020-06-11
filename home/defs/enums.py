from django.db import models


class CourseDifficulty(models.IntegerChoices):
    BEGINNER = 0
    BASIC = 1
    INTERMEDIATE = 2
    PROFICIENT = 3
    ADVANCED = 4


class CourseSubject(models.TextChoices):
    COMPUTER_SCIENCE = 'Computer Science'
    MATH = 'Math'
