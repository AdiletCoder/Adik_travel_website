from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse

from .forms import BloggerRequestForm, CreateCommentForm, UpdatePostForm, CreatePostForm, FoodForm, HotelForm, \
    HotelImageForm
from .models import Hotel, Food, Blogger, Post, ReviewPost, Tag, HotelImage
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView


# class HotelListView(ListView):
#     model = Hotel
#     template_name = 'm_destinations.html'
#     context_object_name = 'hotels'
#     paginate_by = 2
#
#
# class FoodListView(ListView):
#     model = Food
#     template_name = 'm_destinations.html'
#     context_object_name = 'foods'
#     paginate_by = 2


class BloggerRequestView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Blogger
    template_name = 'blogger_request.html'
    form_class = BloggerRequestForm
    success_message = 'Request successfully sent'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = self.request.user
        blogger = form.save(commit=False)
        blogger.user = user
        blogger.save()
        return super().form_valid(form)


def blog_page(request):
    tags = Tag.objects.all()
    posts = Post.objects.all()
    return render(request, 'blog.html', {'tags': tags, 'posts': posts})


class PostListView(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        tag = self.kwargs.get('slug')
        queryset = queryset.filter(tags__slug=tag)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = self.kwargs.get('slug')
        return context


def like_view(request, slug):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('post', args=[str(slug)]))


class PostDetailView(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        stuff = get_object_or_404(Post, slug=self.kwargs['slug'])
        context = super().get_context_data(**kwargs)
        total_likes = stuff.total_likes()
        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True
        context["total_likes"] = total_likes
        context["liked"] = liked
        return context


class PostCreateView(CreateView):
    model = Post
    template_name = 'create_post.html'
    form_class = CreatePostForm
    success_url = reverse_lazy('blog')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_form'] = self.get_form(self.get_form_class())
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.blogger = self.request.user.bloggers.first()
        post.save()
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'update_post.html'
    form_class = UpdatePostForm
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_form'] = self.get_form(self.get_form_class())
        return context


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blogger_confirm_delete.html'
    slug_url_kwarg = 'slug'

    def get_success_url(self):
        from django.urls import reverse
        return reverse('home')


class SearchListView(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'results'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        queryset = queryset.filter(Q(title__icontains=q) | Q(text__icontains=q))
        return queryset


class ReviewIndexPage(ListView):
    model = ReviewPost
    template_name = 'list_comments.html'
    context_object_name = 'list_comments'


class ReviewPostCreateView(CreateView):
    model = ReviewPost
    template_name = 'comment.html'
    form_class = CreateCommentForm

    def form_valid(self, form):
        post = self.kwargs['slug']
        user = self.request.user
        post = Post.objects.get(slug=post)
        comment = form.save(commit=False)
        comment.post = post
        comment.user = user
        comment.save()
        return super().form_valid(form)

    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = self.get_form(self.get_form_class())
        return context


class AddFood(CreateView):
    model = Food
    template_name = 'add_food.html'
    form_class = FoodForm
    success_url = reverse_lazy('profile')


# class AddHotel(CreateView):
#     model = Hotel
#     template_name = 'add_hotel.html'
#     form_class = HotelForm
#     success_url = reverse_lazy('profile')


@login_required
def add_hotel(request):
    ImageFormSet = modelformset_factory(HotelImage, form=HotelImageForm, max_num=5, min_num=1, extra=3)
    if request.method == 'POST':
        form = HotelForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=HotelImage.objects.none())
        if form.is_valid() and formset.is_valid():
            d = form.save(commit=False)
            d.save()
            for f in formset.cleaned_data:
                image = f.get('image')
                if image:
                    HotelImage.objects.create(hotel=d, image=image)
            messages.success(request, 'Hotel created successfully')
            return HttpResponseRedirect(reverse('profile'))
    else:
        form = HotelForm()
        formset = ImageFormSet(queryset=HotelImage.objects.none())
    return render(request, 'add_hotel.html', {'form': form, 'formset': formset})