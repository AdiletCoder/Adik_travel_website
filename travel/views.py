from datetime import datetime

from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView, ListView, UpdateView

from country.models import Country
from facility.models import Hotel, Tag, Post
from place.models import Guide, Place, Service
from .forms import TripForm, ServiceForm, GuideForm, TripUpdateForm
from .models import Trip, Group


def home_page(request):
    places = []
    country = Country.objects.all()

    groups = Group.objects.all()
    for group in groups:
        if group.trips.first() is None:
            group.delete()

    for c in country:
        if c.places.first() is not None:
            places.append(c.places.first())

    tags = Tag.objects.all()
    posts = Post.objects.all().order_by('-date_hub')[:2]
    pop_places = Place.objects.annotate(q_count=Count('trips')).order_by('-q_count')
    top_places = []
    count = 0
    for place in pop_places:
        top_places.append(place)
        if count > 8:
            break
        count += 1
    return render(request, 'index.html', {'places': places, 'tags': tags, 'posts': posts, 'top_places': top_places})


@login_required
def create_trip(request, pk):
    dest = get_object_or_404(Place, id=pk)

    if request.method == 'POST':
        form = TripForm(request.POST, request=request)
        if form.is_valid():
            d = form.save(commit=False)
            d.place = dest
            d.user = request.user
            d.save()
            messages.success(request, 'Trip created successfully')
            return HttpResponseRedirect(reverse('trip-guide', kwargs={'pk': d.pk}))
    else:
        form = TripForm()
        form.fields['guide'].queryset = Guide.objects.filter(place=dest, approved=True)
        form.fields['hotel'].queryset = Hotel.objects.filter(location=dest)
    return render(request, 'create_trip.html', {'form': form})


class MyTripDeleteView(LoginRequiredMixin, DeleteView):
    model = Trip
    template_name = 'blogger_confirm_delete.html'
    success_url = reverse_lazy('profile')
    context_object_name = 'trips'


def trip_service(request, pk):
    trip = get_object_or_404(Trip, id=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=trip)
        if form.is_valid():
            for s in form.cleaned_data['service']:
                trip.service.add(s)
            messages.success(request, 'Services added successfully')
            if trip.type != 'multiple':
                gr = Group.objects.create(type=trip.type, count=1)
                gr.trips.add(trip)
                gr.save()
            else:
                added = False
                groups = Group.objects.filter(type='multiple', count__lte=9)
                same = True
                for group in groups:
                    tr = group.trips.first()
                    if tr.place == trip.place and tr.guide == trip.guide and tr.start_date == trip.start_date \
                            and tr.end_date == trip.end_date and tr.service.all().count() == trip.service.all().count():
                        for service in trip.service.all():
                            if service not in tr.service.all():
                                same = False
                                break

                        if same:
                            trip.group = group
                            group.count = group.count + 1
                            group.save()
                            trip.save()
                            added = True
                            break
                if not added:
                    gr = Group.objects.create(type='multiple', count=1)
                    gr.trips.add(trip)
                    gr.save()
            price = 0
            for sv in trip.service.all():
                price += sv.price
            trip.price = price + trip.hotel.price + trip.meal.price
            if trip.type == 'family':
                trip.price = (trip.price * 10) / 100
            trip.save()
            return HttpResponseRedirect(reverse('destinations'))
    else:
        form = ServiceForm()
        form.fields['service'].queryset = Service.objects.filter(guide=trip.guide)
    return render(request, 'trip_service.html', {'form': form})


def trip_guide(request, pk):
    trip = get_object_or_404(Trip, id=pk)
    groups = []
    for gr in Group.objects.filter(type='multiple'):
        tr = gr.trips.first()
        if tr.start_date == trip.start_date and tr.end_date == trip.end_date and trip.place == tr.place:
            groups.append(gr)

    if request.method == 'POST':
        data = request.POST.get('ava')
        if data:
            group = get_object_or_404(Group, id=data)
            trip_first = group.trips.first()
            trip.guide = trip_first.guide
            for sv in trip_first.service.all():
                trip.service.add(sv)
            price = 0
            for sv in trip_first.service.all():
                price += sv.price
            trip.price = price + trip.hotel.price + trip.meal.price
            trip.save()
            messages.success(request, 'You joined group successfully')
            return HttpResponseRedirect(reverse('profile'))
        else:
            form = GuideForm(request.POST)
            if form.is_valid():
                trip.guide = form.cleaned_data['guide']
                members = form.cleaned_data.get('members', 1)
                if members is None:
                    members = 1
                trip.members = members
                trip.save()
                messages.success(request, 'Services added successfully')
                return HttpResponseRedirect(reverse('trip-service', kwargs={'pk': trip.pk }))
    else:
        form = GuideForm()
        guides = Guide.objects.filter(place=trip.place, approved=True)
        trips = []
        for gr in Group.objects.all():
            trips.append(gr.trips.first())
        guides_list = []
        for tr in trips:
            if tr.start_date <= trip.end_date and tr.end_date >= trip.start_date:
                guides_list.append(tr.guide.pk)
        guides = guides.exclude(id__in=guides_list)
        form.fields['guide'].queryset = guides
    return render(request, 'trip_guide.html', {'form': form, 'groups': groups})


class GroupListView(LoginRequiredMixin, ListView):
    model = Group
    template_name = 'groups.html'
    context_object_name = 'groups'
    paginate_by = 6


class TripUpdateView(UpdateView):
    model = Trip
    template_name = 'change_trip.html'
    form_class = TripUpdateForm
    success_url = reverse_lazy('profile')


def error_404_view(request, exception):
    return render(request, '404.html')


def error_500_view(request, exception):
    return render(request, '404.html')
