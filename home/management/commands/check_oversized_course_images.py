from django.core.management.base import BaseCommand

from home.models import CourseImage


class Command(BaseCommand):
    help = 'Logs to the console course images that are too large'

    def handle(self, *args, **options):
        print("Checking for oversized course images:")

        oversized_images = set()
        for course_image in CourseImage.objects.all():
            img = course_image.image
            if img.width > 320 and img.height > 240:
                oversized_images.add(img)

        if len(oversized_images) > 0:
            for idx, img in enumerate(oversized_images, 1):
                print("{}. {}".format(idx, img.title))
                print("Check complete.")
        else:
            print("No oversized course images.")

