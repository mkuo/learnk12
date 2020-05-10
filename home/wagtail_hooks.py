from taggit.models import Tag
from wagtail.admin.search import SearchArea
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register
)
from wagtail.core import hooks

from home.models.course_review import CourseReview
from home.models.menu_item import MenuItem


class CourseReviewAdmin(ModelAdmin):
    model = CourseReview
    menu_icon = 'form'  # change as required
    menu_order = 350  # (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ['course_detail_page', 'name', 'email', 'publish_date', 'subject', 'score']
    list_filter = ['course_detail_page', 'publish_date', 'reviewer_type', 'score', 'is_anonymous']
    search_fields = ['subject', 'description', 'name', 'email']


class TagAdmin(ModelAdmin):
    model = Tag
    menu_icon = 'tag'  # change as required
    menu_order = 400  # (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ['name', 'slug']
    search_fields = ['name', 'slug']


class MenuItemAdmin(ModelAdmin):
    model = MenuItem
    menu_icon = 'list-ul'
    menu_order = 100
    list_display = ['title', 'page', 'parent_item', 'order']
    list_filter = ['parent_item']
    search_fields = ['title', 'page']
    add_to_settings_menu = True
    exclude_from_explorer = True


modeladmin_register(CourseReviewAdmin)
modeladmin_register(TagAdmin)
modeladmin_register(MenuItemAdmin)


@hooks.register('register_admin_search_area')
def register_frank_search_area():
    return SearchArea('Course Reviews', '/admin/home/coursereview/', classnames='icon icon-form', order=250)


@hooks.register('register_admin_search_area')
def register_frank_search_area():
    return SearchArea('Tags', '/admin/taggit/tag/', classnames='icon icon-tag', order=300)
