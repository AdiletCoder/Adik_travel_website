# Generated by Django 3.2.16 on 2022-12-19 21:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('place', '0006_guide_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guide',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='guides', to=settings.AUTH_USER_MODEL),
        ),
    ]
