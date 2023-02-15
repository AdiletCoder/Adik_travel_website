import datetime

from django import forms
from datetime import date

from .models import Trip


class TripForm(forms.ModelForm):
    start_date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput(attrs={
            'class': 'input datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
    end_date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput(attrs={
            'class': 'input datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )

    class Meta:
        model = Trip
        fields = ('guide', 'hotel', 'meal', 'start_date', 'end_date', 'type')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(TripForm, self).__init__(*args, **kwargs)

    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        start_date = self.cleaned_data.get('start_date')
        age = date.today().year - self.request.user.birth_date.year
        if end_date < start_date:
            raise forms.ValidationError('End date can not be less than start date')
        if age <= 16:
            raise forms.ValidationError('Please, ask your parents to organize a trip you are a kid')
        return end_date


class ServiceForm(forms.ModelForm):
    days = forms.BooleanField(required=False)

    class Meta:
        model = Trip
        fields = ['service', 'days']

    def clean_days(self):
        service = self.cleaned_data.get('service')
        days = self.cleaned_data.get('days')
        start_date = self.instance.start_date
        end_date = self.instance.end_date
        diff = abs((end_date - start_date).days) + 1
        if diff == 1 and len(service) > 6:
            raise forms.ValidationError('I am afraid we can not organize more than 6 services in a day.')
        return days


class TripUpdateForm(forms.ModelForm):

    class Meta:
        model = Trip
        fields = ('hotel', 'meal',)

    def clean_meal(self):
        meal = self.cleaned_data.get('meal')
        trip = self.instance
        start_date = self.instance.start_date
        today = datetime.date.today()
        check = (start_date - today).days
        if check < 2 and meal != trip.meal:
            raise forms.ValidationError('You can not change the type of food before two days left to the trip')
        return meal


class GuideForm(forms.ModelForm):
    members = forms.IntegerField(required=False)

    class Meta:
        model = Trip
        fields = ['members', 'guide']

    def clean_members(self):
        members = self.cleaned_data.get('members', 1)
        return members
