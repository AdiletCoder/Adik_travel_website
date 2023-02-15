from django import forms
from account.models import User
from place.models import Guide


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(min_length=8, required=True, widget=forms.PasswordInput)

    birth_date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput(attrs={
            'class': 'input datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'birth_date', 'email', 'password')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('User with given email already exists')
        return email

    def save(self):
        user = User.objects.create_user(**self.cleaned_data)
        return user


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'input-file', 'name': 'picture'}))
    birth_date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput(attrs={
            'class': 'input datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'birth_date', 'avatar']


class UpdateGuideForm(forms.ModelForm):
    class Meta:
        model = Guide
        fields = ('description', 'experience', 'language', 'place',)
