# Generated by Django 5.2.4 on 2025-07-10 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_booking_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='travel_date',
            field=models.DateField(null=True),
        ),
    ]
