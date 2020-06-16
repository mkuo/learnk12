from django.forms import ModelForm, Textarea

from home.models import SiteFeedback


class SiteFeedbackForm(ModelForm):
    class Meta:
        model = SiteFeedback
        fields = ['category', 'description', 'name', 'email']
        widgets = {
            'category': Textarea(attrs={'rows': 1}),
            'description': Textarea(attrs={'rows': 4}),
        }
