# Generated by Django 4.0.6 on 2022-09-21 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brewguide', '0002_location_shop_reviews_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='location',
            field=models.TextField(default='default'),
            preserve_default=False,
        ),
    ]