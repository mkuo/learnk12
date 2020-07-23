from django.forms import ModelForm, BooleanField
from home.models import TutorPage


class TutorForm(ModelForm):
    public = BooleanField(required=False)
    is_accepting_students = BooleanField(required=False)

    class Meta:
        model = TutorPage
        fields = (
            'course_subjects', 'hourly_rate', 'timezone', 'description',
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.title = self.user
        super(TutorForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance.title = self.title
        self.instance.user = self.user
        return super().save(commit=commit)


class UpdateTutorForm(ModelForm):
    public = BooleanField(required=False)
    is_accepting_students = BooleanField(required=False)

    class Meta:
        model = TutorPage
        fields = (
            'course_subjects', 'hourly_rate', 'timezone', 'description',
        )
