# Generated by Django 4.0.1 on 2022-09-28 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brewguide', '0005_shop_coverimage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='location',
            new_name='name',
        ),
    ]