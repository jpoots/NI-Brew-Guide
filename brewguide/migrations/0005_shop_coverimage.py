# Generated by Django 4.0.1 on 2022-09-27 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brewguide', '0004_rename_images_image_rename_reviews_review_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='coverImage',
            field=models.ImageField(default=123, upload_to='brewguide'),
            preserve_default=False,
        ),
    ]
