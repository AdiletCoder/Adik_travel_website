import datetime

from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from account.forms import RegistrationForm, UpdateProfileForm, UpdateGuideForm
from account.models import User
from django.contrib.auth.decorators import login_required

from place.models import Guide
from place.forms import ServiceForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from travel.models import Trip


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'account/password_reset.html'
    email_template_name = 'account/password_reset_email.html'
    subject_template_name = 'account/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('home')


class RegisterView(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'account/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')
    success_message = 'Successfully registered'


class SignInView(LoginView):
    template_name = 'account/login.html'
    success_url = reverse_lazy('home')
    success_message = 'Successfully logged in'


@login_required
def profile(request):
    guide = None
    guide_trips = None
    trips = Trip.objects.filter(end_date__gte=datetime.date.today())
    completed_trips = Trip.objects.filter(end_date__lt=datetime.date.today(), user=request.user)
    if request.user.is_guide:
        guide = Guide.objects.filter(user=request.user, approved=True).first()
        guide_trips = Trip.objects.filter(guide=guide)

    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile is updated successfully')
    else:
        form = UpdateProfileForm(instance=request.user)

    return render(request, 'account/myprofile.html', {'form': form, 'completed_trips': completed_trips,
                                                      'user': request.user, 'guide': guide, 'trips':trips,
                                                      'guide_trips': guide_trips})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account/change_password.html', {
        'form': form
    })


def add_service(request,):
    if request.method == 'POST':
        form = ServiceForm(request.POST)

        if form.is_valid():
            service = form.save(commit=False)
            service.guide = request.user.guides.first()
            service.place = request.user.guides.first().place
            service.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
    else:
        form = ServiceForm()
    return render(request, 'account/add_service.html', {
        'form': form
    })