# Generated by Django 3.2.16 on 2022-12-17 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='currency',
            field=models.CharField(default='USD', max_length=50),
        ),
    ]
