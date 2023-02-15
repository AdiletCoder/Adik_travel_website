from django.db import models

from account.models import User
from country.models import Language
from place.models import Place


class Hotel(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=9)
    location = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="hotels")

    def __str__(self):
        return self.name


class Food(models.Model):
    FOOD_TYPES = (
        ("halal", "Halal"),
        ("vegetarian", "Vegetarian"),
        ("vegan", "Vegan"),
        ("any", "Any"),
    )
    type = models.CharField(choices=FOOD_TYPES, default="any", max_length=150)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=9)

    def __str__(self):
        return self.type


class Blogger(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bloggers')
    description = models.TextField()
    language = models.ManyToManyField(Language, related_name='bloggers')
    approved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name


class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(primary_key=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null=True)

    def __str__(self):
        if self.parent:
            return f'{self.parent} --> {self.title}'
        return self.title


class Post(models.Model):
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    title = models.CharField(max_length=150)
    text = models.TextField()
    image = models.ImageField(upload_to='posts')
    date_hub = models.DateTimeField(auto_now_add=True)
    blogger = models.ForeignKey(Blogger, related_name='posts', on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='blog_posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    @property
    def get_image(self):
        return self.image.url

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('post', kwargs={'slug': self.slug})


class ReviewPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='commentaries', verbose_name='Post')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments', verbose_name='User')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def str(self):
        return f'{self.user}: {self.post}'

    class Meta:
        ordering = ['-created']


class HotelImage(models.Model):
    image = models.ImageField(upload_to="places", verbose_name="pictures", null=True, blank=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="pictures")

    def __str__(self):
        return self.image.url
