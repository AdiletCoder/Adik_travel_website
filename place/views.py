from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin

from .models import Place, Guide, Comment
from .forms import GuideRequestForm, CommentModelForm
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView


class PlaceListView(ListView):
    model = Place
    template_name = 'destinations.html'
    context_object_name = 'destinations'
    paginate_by = 6


class PlaceDetailView(FormMixin, DetailView):
    model = Place
    template_name = 'destination.html'
    context_object_name = 'place'
    form_class = CommentModelForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rel_places'] = Place.objects.filter(country=self.object.country).exclude(id=self.object.id)[:2]
        context['comments'] = self.object.comment.filter(is_approved=True)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.place = self.object
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()

    def get_success_url(self):
        return reverse('destination', kwargs={'pk': self.get_context_data()['place'].pk})


class GuideRequestView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Guide
    template_name = 'guide_request.html'
    form_class = GuideRequestForm
    success_message = 'Request successfully sent'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = self.request.user
        guide = form.save(commit=False)
        guide.user = user
        guide.save()
        return super().form_valid(form)


class PlaceSearchListView(ListView):
    model = Place
    template_name = 'search-places.html'
    context_object_name = 'place_results'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        queryset = queryset.filter(Q(name__icontains=q) | Q(description__icontains=q))
        return queryset


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('destination', pk=comment.place.pk)
