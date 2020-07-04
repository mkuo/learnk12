from django.core.management.base import BaseCommand
from wagtail.images.models import Image

from home.models import InfoPage


class Command(BaseCommand):
    help = 'Logs to the console images that are not used'

    '''
    StreamFields are json fields that are not captured in get_usage()
    so we have to search for and remove them explicitly
    '''
    @staticmethod
    def check_streamfield(unused_images, page_model, block_type):
        for page in page_model.objects.all():
            for block in page.body:
                if block.block_type != block_type:
                    continue
                for img in block.value:
                    if img in unused_images:
                        unused_images.remove(img)

    def handle(self, *args, **options):
        print("Checking for unused images:")

        unused_images = []
        for img in Image.objects.all():
            if not img.get_usage():
                unused_images.append(img)

        if len(unused_images) > 0:
            self.check_streamfield(unused_images, InfoPage, 'image_row')
            for idx, img in enumerate(unused_images, 1):
                print("{}. {}".format(idx, img.title))
            print("Check complete.")
        else:
            print("No unused images.")

