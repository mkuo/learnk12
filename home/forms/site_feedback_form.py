from django.forms import ModelForm, Textarea

from home.models import SiteFeedback


class SiteFeedbackForm(ModelForm):
    class Meta:
        model = SiteFeedback
        fields = ['subject', 'description', 'name', 'email']
        widgets = {
            'subject': Textarea(attrs={'rows': 1}),
            'description': Textarea(attrs={'rows': 4}),
        }
