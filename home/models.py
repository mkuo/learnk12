from wagtail.core.models import Page

from home.submodels.course_detail_page import CourseDetailPage
from home.submodels.course_image import CourseImage
from home.submodels.course_review import CourseReview
from home.submodels.course_tag import CourseTag
from home.submodels.courses_page import CoursesPage
from home.submodels.home_page import HomePage
from home.submodels.tutor_detail_page import TutorDetailPage
from home.submodels.tutors_page import TutorsPage

Page.subpage_types = ['home.HomePage']
