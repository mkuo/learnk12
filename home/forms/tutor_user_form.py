from django.forms import ModelForm
from home.models import TutorPage


class TutorForm(ModelForm):

    class Meta:
        model = TutorPage
        fields = (
            'title', 'course_subjects', 'hourly_rate', 'timezone', 'description', 'is_accepting_students', 'public'
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(TutorForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance.user = self.user
        return super().save(commit=commit)


class UpdateTutorForm(ModelForm):
    class Meta:
        model = TutorPage
        fields = (
            'title', 'course_subjects', 'hourly_rate', 'timezone', 'description', 'is_accepting_students', 'public',
        )
