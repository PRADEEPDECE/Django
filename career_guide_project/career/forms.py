from django import forms
from .models import Goal


class CareerTestForm(forms.Form):
    interests = forms.CharField(widget=forms.Textarea, help_text="Describe your interests")
    skills = forms.CharField(widget=forms.Textarea, help_text="Describe your skills")
    education = forms.CharField(widget=forms.Textarea, help_text="Describe your education/background")
    preferences = forms.CharField(widget=forms.Textarea, required=False, help_text="Work preferences, location, etc.")


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ["title", "description"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3
            }),
        }
