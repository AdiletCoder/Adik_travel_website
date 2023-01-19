from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DeleteView, ListView, DetailView, UpdateView
from django.forms import modelformset_factory

from facility.models import Blogger
from place.models import Image, Guide
from place.views import Place
from .forms import PlaceEditForm, ImageForm, PlaceForm


# Moderator Place Views
class PlaceDeleteView(LoginRequiredMixin, DeleteView):
    model = Place
    template_name = 'blogger_confirm_delete.html'
    success_url = reverse_lazy('m-places')
    context_object_name = 'destination'


class PlaceListView(LoginRequiredMixin, ListView):
    model = Place
    template_name = 'm_destinations.html'
    context_object_name = 'destinations'
    paginate_by = 6


class PlaceDetailView(LoginRequiredMixin, DetailView):
    model = Place
    template_name = 'm_destination.html'
    context_object_name = 'place'
    # extra_context = {'words': Comment.objects.all()}


class PlaceUpdateView(LoginRequiredMixin, UpdateView):
    model = Place
    template_name = 'edit_destination.html'
    form_class = PlaceEditForm
    context_object_name = 'destination'
    success_url = reverse_lazy('m-places')


@login_required
def add_destination(request):
    ImageFormSet = modelformset_factory(Image, form=ImageForm, max_num=5, min_num=1, extra=3)
    if request.method == 'POST':
        form = PlaceForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())
        if form.is_valid() and formset.is_valid():
            d = form.save(commit=False)
            d.save()
            for f in formset.cleaned_data:
                image = f.get('image')
                if image:
                    Image.objects.create(place=d, image=image)
            messages.success(request, 'Destination created successfully')
            return HttpResponseRedirect(reverse('destinations'))
    else:
        form = PlaceForm()
        formset = ImageFormSet(queryset=Image.objects.none())
    return render(request, 'add_destination.html', {'form': form, 'formset': formset})
# End of places


@login_required
def approve_guide(request):
    if request.method == 'POST':
        data = request.POST.get('accept').split(' ')
        guide_id = data[1]

        approved = False
        is_blogger = False

        if 'accept' in data[0]:
            approved = True
        if str(data[0]).endswith('b'):
            is_blogger = True

        if approved:
            if not is_blogger:
                guide = Guide.objects.get(id=guide_id)
                user = guide.user
                user.is_guide = True
                user.save()
                guide.approved = True
                guide.save()
                messages.success(request, "Guide's request approved successfully")

            else:
                guide = Blogger.objects.get(id=guide_id)
                user = guide.user
                user.is_blogger = True
                user.save()
                guide.approved = True
                guide.save()
                messages.success(request, "Blogger's request approved successfully")

        else:
            if not is_blogger:
                guide = Guide.objects.get(id=guide_id)
                guide.user.is_guide = False
                guide.user.save()
                guide.delete()
                messages.success(request, "Guide's request declined successfully")

            else:
                guide = Blogger.objects.get(id=guide_id)
                guide.user.is_blogger = False
                guide.user.save()
                guide.delete()
                messages.success(request, "Blogger's request declined successfully")

        return HttpResponseRedirect(reverse('m-approve-guide'))
    else:
        guides = Guide.objects.filter(approved=False).order_by('-created')
        bloggers = Blogger.objects.filter(approved=False).order_by('-created')

        return render(request, 'guide_approve.html', {'guides': guides, 'bloggers': bloggers})


class BloggerListView(ListView):
    model = Blogger
    template_name = 'm_bloggers.html'
    context_object_name = 'bloggers'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(approved=True)
        return queryset


class BloggerDeleteView(DeleteView):
    model = Blogger
    template_name = 'blogger_confirm_delete.html'
    success_url = reverse_lazy('m-bloggers')

    def delete(self, request, *args, **kwargs):
        object = self.get_object()
        object.user.is_blogger = False
        object.user.save()
        return super().delete(request, *args, **kwargs)


class GuideListView(ListView):
    model = Guide
    template_name = 'm_guides.html'
    context_object_name = 'guides'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(approved=True)
        return queryset


class GuideDeleteView(DeleteView):
    model = Guide
    template_name = 'blogger_confirm_delete.html'
    success_url = reverse_lazy('m-guides')

    def delete(self, request, *args, **kwargs):
        object = self.get_object()
        object.user.is_guide = False
        object.user.save()
        return super().delete(request, *args, **kwargs)

