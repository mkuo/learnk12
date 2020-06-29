from django.db import models


class CourseDifficulty(models.IntegerChoices):
    EASY = 0
    MEDIUM = 1
    HARD = 2


class CourseSubject(models.TextChoices):
    COMPUTER_SCIENCE = 'Computer Science'
    MATH = 'Math'


class AgeGroup(tuple, models.Choices):
    # enum = min age, max age, label
    EARLY = 3, 6, "Early Education, ages 3 to 6"
    PRIMARY = 7, 10, "Primary School, ages 7 to 10"
    MIDDLE = 11, 13, "Middle School, ages 11 to 13"
    HIGH = 14, 17, "High School, ages 14 to 17"
    ADVANCED = 18, 99, "Advanced, ages 18+"


class CostInterval(models.TextChoices):
    LIFETIME = 'once'
    WEEK = 'wk'
    MONTH = 'mo'
    QUARTER = 'qtr'
    YEAR = 'yr'
