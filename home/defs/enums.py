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
    ('GMT', 'GMT Casablanca'),
    ('GMT', 'GMT Coordinated Universal Time'),
    ('GMT', 'GMT Greenwich Mean Time : Dublin, Edinburgh, Lisbon, London'),
    ('GMT', 'GMT Monrovia, Reykjavik'),
    ('GMT+01:00', 'GMT+01:00 Amsterdam, Berlin, Bern, Rome, Stockholm, Vienna'),
    ('GMT+01:00', 'GMT+01:00 Belgrade, Bratislava, Budapest, Ljubljana, Prague'),
    ('GMT+01:00', 'GMT+01:00 Brussels, Copenhagen, Madrid, Paris'),
    ('GMT+01:00', 'GMT+01:00 Sarajevo, Skopje, Warsaw, Zagreb'),
    ('GMT+01:00', 'GMT+01:00 West Central Africa'),
    ('GMT+02:00', 'GMT+02:00 Amman'),
    ('GMT+02:00', 'GMT+02:00 Athens, Bucharest, Istanbul'),
    ('GMT+02:00', 'GMT+02:00 Beirut'),
    ('GMT+02:00', 'GMT+02:00 Cairo'),
    ('GMT+02:00', 'GMT+02:00 Damascus'),
    ('GMT+02:00', 'GMT+02:00 Harare, Pretoria'),
    ('GMT+02:00', 'GMT+02:00 Helsinki, Kyiv, Riga, Sofia, Tallinn, Vilnius'),
    ('GMT+02:00', 'GMT+02:00 Jerusalem'),
    ('GMT+02:00', 'GMT+02:00 Minsk'),
    ('GMT+02:00', 'GMT+02:00 Windhoek'),
    ('GMT+03:00', 'GMT+03:00 Baghdad'),
    ('GMT+03:00', 'GMT+03:00 Kuwait, Riyadh'),
    ('GMT+03:00', 'GMT+03:00 Moscow, St. Petersburg, Volgograd'),
    ('GMT+03:00', 'GMT+03:00 Nairobi'),
    ('GMT+03:30', 'GMT+03:00 Tehran'),
    ('GMT+04:00', 'GMT+04:00 Abu Dhabi, Muscat'),
    ('GMT+04:00', 'GMT+04:00 Baku'),
    ('GMT+04:00', 'GMT+04:00 Port Louis'),
    ('GMT+04:00', 'GMT+04:00 Tbilisi'),
    ('GMT+04:00', 'GMT+04:00 Yerevan'),
    ('GMT+04:30', 'GMT+04:30 Kabul'),
    ('GMT+05:00', 'GMT+05:00 Ekaterinburg'),
    ('GMT+05:00', 'GMT+05:00 Islamabad, Karachi'),
    ('GMT+05:00', 'GMT+05:00 Tashkent'),
    ('GMT+05:30', 'GMT+05:30 Chennai, Kolkata, Mumbai, New Delhi'),
    ('GMT+05:30', 'GMT+05:30 Sri Jayawardenepura'),
    ('GMT+05:45', 'GMT+05:45 Kathmandu'),
    ('GMT+06:00', 'GMT+06:00 Astana'),
    ('GMT+06:00', 'GMT+06:00 Dhaka'),
    ('GMT+06:00', 'GMT+06:00 Novosibirsk'),
    ('GMT+06:30', 'GMT+06:30 Yangon (Rangoon)'),
    ('GMT+07:00', 'GMT+07:00 Bangkok, Hanoi, Jakarta'),
    ('GMT+07:00', 'GMT+07:00 Krasnoyarsk'),
    ('GMT+08:00', 'GMT+08:00 Beijing, Chongqing, Hong Kong, Urumqi'),
    ('GMT+08:00', 'GMT+08:00 Irkutsk'),
    ('GMT+08:00', 'GMT+08:00 Kuala Lumpur, Singapore'),
    ('GMT+08:00', 'GMT+08:00 Perth'),
    ('GMT+08:00', 'GMT+08:00 Taipei'),
    ('GMT+08:00', 'GMT+08:00 Ulaanbaatar'),
    ('GMT+09:00', 'GMT+09:00 Osaka, Sapporo, Tokyo'),
    ('GMT+09:00', 'GMT+09:00 Seoul'),
    ('GMT+09:00', 'GMT+09:00 Yakutsk'),
    ('GMT+09:30', 'GMT+09:30 Adelaide'),
    ('GMT+09:30', 'GMT+09:30 Darwin'),
    ('GMT+10:00', 'GMT+10:00 Brisbane'),
    ('GMT+10:00', 'GMT+10:00 Canberra, Melbourne, Sydney'),
    ('GMT+10:00', 'GMT+10:00 Guam, Port Moresby'),
    ('GMT+10:00', 'GMT+10:00 Hobart'),
    ('GMT+10:00', 'GMT+10:00 Vladivostok'),
    ('GMT+11:00', 'GMT+11:00 Magadan, Solomon Is., New Caledonia'),
    ('GMT+12:00', 'GMT+12:00 Auckland, Wellington'),
    ('GMT+12:00', 'GMT+12:00 Coordinated Universal Time+12'),
    ('GMT+12:00', 'GMT+12:00 Fiji'),
    ('GMT+12:00', 'GMT+12:00 Petropavlovsk-Kamchatsky - Old'),
    ('GMT+13:00', 'GMT+13:00 Nuku alofa'),
    ('GMT-01:00', 'GMT-01:00 Azores'),
    ('GMT-01:00', 'GMT-01:00 Cape Verde Is.'),
    ('GMT-02:00', 'GMT-02:00 Coordinated Universal Time-02'),
    ('GMT-02:00', 'GMT-02:00 Mid-Atlantic'),
    ('GMT-03:00', 'GMT-03:00 Brasilia'),
    ('GMT-03:00', 'GMT-03:00 Buenos Aires'),
    ('GMT-03:00', 'GMT-03:00 Cayenne, Fortaleza'),
    ('GMT-03:00', 'GMT-03:00 Greenland'),
    ('GMT-03:00', 'GMT-03:00 Montevideo'),
    ('GMT-03:30', 'GMT-03:30 Newfoundland'),
    ('GMT-04:00', 'GMT-04:00 Asuncion'),
    ('GMT-04:00', 'GMT-04:00 Atlantic Time (Canada)'),
    ('GMT-04:00', 'GMT-04:00 Cuiaba'),
    ('GMT-04:00', 'GMT-04:00 Georgetown, La Paz, Manaus, San Juan'),
    ('GMT-04:00', 'GMT-04:00 Santiago'),
    ('GMT-04:30', 'GMT-04:30 Caracas'),
    ('GMT-05:00', 'GMT-05:00 Bogota, Lima, Quito'),
    ('GMT-05:00', 'GMT-05:00 Eastern Time (US & Canada)'),
    ('GMT-05:00', 'GMT-05:00 Indiana (East)'),
    ('GMT-06:00', 'GMT-06:00 Central America'),
    ('GMT-06:00', 'GMT-06:00 Central Time (US & Canada)'),
    ('GMT-06:00', 'GMT-06:00 Guadalajara, Mexico City, Monterrey'),
    ('GMT-06:00', 'GMT-06:00 Saskatchewan'),
    ('GMT-07:00', 'GMT-07:00 Arizona'),
    ('GMT-07:00', 'GMT-07:00 Chihuahua, La Paz, Mazatlan'),
    ('GMT-07:00', 'GMT-07:00 Mountain Time (US & Canada)'),
    ('GMT-08:00', 'GMT-08:00 Baja California'),
    ('GMT-08:00', 'GMT-08:00 Pacific Time (US & Canada)'),
    ('GMT-09:00', 'GMT-09:00 Alaska'),
    ('GMT-10:00', 'GMT-10:00 Hawaii'),
    ('GMT-11:00', 'GMT-11:00 Coordinated Universal Time-11'),
    ('GMT-11:00', 'GMT-11:00 Samoa'),
    ('GMT-12:00', 'GMT-12:00 International Date Line West')
)
