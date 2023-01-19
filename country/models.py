from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=150)
    language = models.ManyToManyField(Language, related_name="languages")
    currency = models.CharField(max_length=50, default='USD')

    def __str__(self):
        return self.name




