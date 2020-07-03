from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class ImageBlock(ImageChooserBlock):
    class Meta:
        template = 'home/blocks/imagechooser_block.html'
        icon = "edit"
        label = "Image"


class RichTextBlock(blocks.RichTextBlock):
    class Meta:
        template = 'home/blocks/richtext_block.html'
        icon = "edit"
        label = "RichText"
