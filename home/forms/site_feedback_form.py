from django.forms import ModelForm, Textarea, HiddenInput

from home.models import SiteFeedback


class SiteFeedbackForm(ModelForm):
    class Meta:
        model = SiteFeedback
        fields = ['subject', 'description', 'name', 'email']
        widgets = {
            'subject': Textarea(attrs={'rows': 1}),
            'description': Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(SiteFeedbackForm, self).__init__(*args, **kwargs)
        if not self.user:
            self.fields['name'].required = True
            self.fields['email'].required = True
        else:
            self.fields['name'].widget = HiddenInput()
            self.fields['email'].widget = HiddenInput()
