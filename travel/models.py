from django.db import models

from account.models import User
from facility.models import Hotel, Food
from place.models import Place, Guide, Service


class Group(models.Model):
    GROUP_TYPES = (
        ("single", "Single"),
        ("multiple", "Multiple"),
        ("family", "Family group"),
    )

    type = models.CharField(choices=GROUP_TYPES, default='multiple', max_length=150)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.type


class Trip(models.Model):
    TRIP_TYPES = (
        ("single", "Single"),
        ("multiple", "Multiple"),
        ("family", "Family group"),
    )

    user = models.ForeignKey(User, related_name='trips', on_delete=models.CASCADE)
    place = models.ForeignKey(Place, related_name='trips', on_delete=models.CASCADE)
    guide = models.ForeignKey(Guide, related_name='trips', on_delete=models.CASCADE, null=True, blank=True)
    hotel = models.ForeignKey(Hotel, related_name='trips', on_delete=models.CASCADE)
    meal = models.ForeignKey(Food, related_name='trips', on_delete=models.CASCADE)
    type = models.CharField(choices=TRIP_TYPES, default='multiple', max_length=150)
    group = models.ForeignKey(Group, related_name='trips', blank=True, null=True, on_delete=models.DO_NOTHING)
    service = models.ManyToManyField(Service, related_name='trips')
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    members = models.PositiveIntegerField(default=1)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.place.name
