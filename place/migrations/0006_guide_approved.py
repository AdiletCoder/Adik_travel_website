# Generated by Django 3.2.16 on 2022-12-19 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('place', '0005_guide'),
    ]

    operations = [
        migrations.AddField(
            model_name='guide',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
