# Generated by Django 3.2.16 on 2023-01-11 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.FileField(default='avatars/my_photo.jpg', upload_to='avatars'),
        ),
    ]