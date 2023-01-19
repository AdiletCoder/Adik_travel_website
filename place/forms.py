from django import forms
from .models import Guide, Service, Comment


class GuideRequestForm(forms.ModelForm):
    class Meta:
        model = Guide
        fields = ('description', 'experience', 'language', 'place')

    def clean_place(self):
        place = self.cleaned_data.get('place')
        languages = self.cleaned_data.get('language')
        go_on = False
        for lang in languages:
            if lang in place.country.language.all():
                go_on = True
                break
        if not go_on:
            raise forms.ValidationError('Unfortunately, we can not give you permission to guide, '
                                        'since you can not speak language that is required for chosen place')
        return place


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('name', 'description', 'price')


class CommentModelForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = [
            'message',
        ]
