from taggit.models import Tag
from wagtail.admin.search import SearchArea
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register
)
from wagtail.core import hooks


class TagAdmin(ModelAdmin):
    model = Tag
    menu_icon = 'tag'  # change as required
    menu_order = 400  # (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ['name', 'slug']
    search_fields = ['name', 'slug']


# Now you just need to register your customised ModelAdmin class with Wagtail
modeladmin_register(TagAdmin)


@hooks.register('register_admin_search_area')
def register_frank_search_area():
    return SearchArea('Tags', '/admin/taggit/tag/', classnames='icon icon-tag', order=300)
