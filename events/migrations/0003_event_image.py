# Generated by Django 5.1.7 on 2025-03-28 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_event_event_date_alter_event_event_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='events/images/'),
        ),
    ]
