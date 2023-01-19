from django import forms

from country.models import Language, Country


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = '__all__'


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = '__all__'
