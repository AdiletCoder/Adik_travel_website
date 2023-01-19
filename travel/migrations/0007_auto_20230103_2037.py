# Generated by Django 3.2.16 on 2023-01-03 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0006_group_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='type',
            new_name='group_type',
        ),
        migrations.AddField(
            model_name='trip',
            name='type',
            field=models.CharField(choices=[('single', 'Single'), ('multiple', 'Multiple')], default='multiple', max_length=150),
        ),
    ]