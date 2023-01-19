from django import forms
from place.models import Place, Image


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = '__all__'


class PlaceEditForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ['name', 'description', 'country', 'map']


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image', )
