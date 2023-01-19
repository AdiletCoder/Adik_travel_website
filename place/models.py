from django.conf import settings
from django.db import models

from country.models import Country, Language
from account.models import User


class Place(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="places")
    map = models.TextField(max_length=5000, null=True, blank=True)

    @property
    def get_image(self):
        return self.pictures.first()

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(upload_to="places", verbose_name="pictures", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="pictures")

    def __str__(self):
        return self.image.url


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user', verbose_name='User')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='comment')
    message = models.TextField(max_length=1500)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return self.message
# class Comment(models.Model):
#     author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='words', on_delete=models.CASCADE)
#     fundraiser = models.ForeignKey(Place, related_name='words', on_delete=models.CASCADE)
#     body = models.TextField()
#     created = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.body
#
#     class Meta:
#         ordering = ('-created',)


class Guide(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='guides')
    description = models.TextField()
    experience = models.TextField()
    language = models.ManyToManyField(Language, related_name='guides')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='guides')
    approved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name


class Service(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    place = models.ForeignKey(Place, related_name="services", on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=9)
    guide = models.ForeignKey(Guide, related_name='services', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
