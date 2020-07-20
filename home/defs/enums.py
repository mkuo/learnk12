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


TIMEZONE = (
    ('UTC−12:00', 'UTC−12:00'),
    ('UTC−11:00', 'UTC−11:00'),
    ('UTC−10:00', 'UTC−10:00'),
    ('UTC−9:30', 'UTC−9:30'),
    ('UTC−9:00', 'UTC−9:00'),
    ('UTC−8:00', 'UTC−8:00'),
    ('UTC−7:00', 'UTC−7:00'),
    ('UTC−6:00', 'UTC−6:00'),
    ('UTC−5:00', 'UTC−5:00'),
    ('UTC−4:00', 'UTC−4:00'),
    ('UTC−3:30', 'UTC−3:30'),
    ('UTC−3:00', 'UTC−3:00'),
    ('UTC−2:00', 'UTC−2:00'),
    ('UTC−1:00', 'UTC−1:00'),
    ('UTC−00:00', 'UTC−00:00'),
    ('UTC+1:00', 'UTC+1:00'),
    ('UTC+2:00', 'UTC+2:00'),
    ('UTC+3:00', 'UTC+3:00'),
    ('UTC+3:30', 'UTC+3:30'),
    ('UTC+4:00', 'UTC+4:00'),
    ('UTC+4:30', 'UTC+4:30'),
    ('UTC+5:00', 'UTC+5:00'),
    ('UTC+5:30', 'UTC+5:30'),
    ('UTC+5:45', 'UTC+5:45'),
    ('UTC+6:00', 'UTC+6:00'),
    ('UTC+6:30', 'UTC+6:30'),
    ('UTC+7:00', 'UTC+7:00'),
    ('UTC+8:00', 'UTC+8:00'),
    ('UTC+8:45', 'UTC+8:45'),
    ('UTC+9:00', 'UTC+9:00'),
    ('UTC+9:30', 'UTC+9:30'),
    ('UTC+10:00', 'UTC+10:00'),
    ('UTC+10:30', 'UTC+10:30'),
    ('UTC+11:00', 'UTC+11:00'),
    ('UTC+12:00', 'UTC+12:00'),
    ('UTC+12:45', 'UTC+12:45'),
    ('UTC+13:00', 'UTC+13:00'),
    ('UTC+14:00', 'UTC+14:00'),
)
