from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from country.forms import LanguageForm, CountryForm
from country.models import Language, Country


class AddLanguage(CreateView):
    template_name = 'add_language.html'
    model = Language
    form_class = LanguageForm
    success_url = reverse_lazy('profile')


class AddCountry(CreateView):
    model = Country
    template_name = 'add_country.html'
    form_class = CountryForm
    success_url = reverse_lazy('profile')
