from django.core.management.base import BaseCommand

from home.models import CourseReview, SiteFeedback
from user_auth.models import User


class Command(BaseCommand):
    help = 'Logs to the console users and CourseReviews and SiteFeedback that have the same email but are not already ' \
           'joined '

    def handle(self, *args, **options):
        print("Checking for unjoined course reviews:")
        for user in User.objects.all():
            course_reviews = CourseReview.objects.filter(email=user.email).all()
            if course_reviews:
                print('{} course reviews for join'.format(len(course_reviews)))
                course_reviews.update(email=None, name=None, user=user)
            else:
                print("No unjoined course reviews for {}.".format(user))
            site_feedback = SiteFeedback.objects.filter(email=user.email).all()
            if site_feedback:
                print('{} site feedback for join'.format(len(site_feedback)))
                site_feedback.update(email=None, name=None, user=user)
            else:
                print("No unjoined site feedback for {}.".format(user))
        print("Check complete.")

