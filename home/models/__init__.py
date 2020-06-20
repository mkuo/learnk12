from wagtail.core.models import Page

from .all_courses_page import AllCoursesPage
from .all_providers_page import AllProvidersPage
from .course_page import CoursePage
from .course_image import CourseImage
from .course_review import CourseReview
from .course_tags import LessonType, Platform, ProgrammingLanguage
from .course_subject_page import CourseSubjectPage
from .home_page import HomePage
from .info_page import InfoPage
from .provider_page import ProviderPage
from .site_feedback import SiteFeedback
from .site_feedback_page import SiteFeedbackPage
from .tutor_detail_page import TutorDetailPage
from .tutors_page import TutorsPage

# set HomePage as only page under root
Page.subpage_types = ['home.HomePage']
