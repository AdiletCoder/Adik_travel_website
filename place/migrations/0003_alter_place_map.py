# Generated by Django 3.2.16 on 2022-12-17 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('place', '0002_place_map'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='map',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
