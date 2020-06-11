from wagtail.core.models import Page

from .course_detail_page import CourseDetailPage
from .course_image import CourseImage
from .course_review import CourseReview
from .course_tag import CourseTag
from .course_subject_page import CourseSubjectPage
from .home_page import HomePage
from .info_page import InfoPage
from .tutor_detail_page import TutorDetailPage
from .tutors_page import TutorsPage

# set HomePage as only page under root
Page.subpage_types = ['home.HomePage']
