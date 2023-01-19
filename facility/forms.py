from django import forms
from .models import Blogger, Post, ReviewPost, Food, Hotel, HotelImage


class BloggerRequestForm(forms.ModelForm):
    class Meta:
        model = Blogger
        fields = ('description', 'language')


# class ServiceForm(forms.ModelForm):
#     class Meta:
#         model = Service
#         fields = ('name', 'description', 'price')


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'slug', 'text', 'image', 'tags',)


class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'slug', 'text', 'image', 'tags',)


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = ReviewPost
        fields = ('body',)

        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = '__all__'


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = '__all__'


class HotelImageForm(forms.ModelForm):
    class Meta:
        model = HotelImage
        fields = ('image', )

