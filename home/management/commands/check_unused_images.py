from sys import stdout

from django.core.management.base import BaseCommand
from django.db import connection
from django.db.models.signals import post_save, post_delete
from wagtail.images.models import Image

from home.models.course_review import CourseReview


class Command(BaseCommand):
    help = 'Logs to the console Images that are not used'

    def handle(self, *args, **options):
        print("Checking for unused Images:")
        i = 1
        for img in Image.objects.all():
            if not img.get_usage():
                print("{}. {}".format(i, img.title))
                i += 1
        print("Check complete.")
