# Generated by Django 5.1.7 on 2025-03-28 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_date',
            field=models.DateField(default='2025-01-01'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_time',
            field=models.TimeField(),
        ),
    ]
