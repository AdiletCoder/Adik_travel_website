from django import forms
from account.models import User
from place.models import Guide


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(min_length=8, required=True, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'age', 'email', 'password')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('User with given email already exists')
        return email

    def save(self):
        user = User.objects.create_user(**self.cleaned_data)
        return user


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file', 'name': 'picture'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'age', 'avatar']


class UpdateGuideForm(forms.ModelForm):
    class Meta:
        model = Guide
        fields = ('description', 'experience', 'language', 'place',)
