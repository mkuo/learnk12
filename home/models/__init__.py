from wagtail.core.models import Page

from .course_detail_page import CourseDetailPage
from .course_image import CourseImage
from .course_review import CourseReview
from .course_tag import CourseTag
from .courses_page import CoursesPage
from .home_page import HomePage
from .tutor_detail_page import TutorDetailPage
from .tutors_page import TutorsPage

Page.subpage_types = ['home.HomePage']
