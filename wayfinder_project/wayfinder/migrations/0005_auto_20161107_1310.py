# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-07 13:10
from __future__ import unicode_literals

from django.db import migrations, models
import wayfinder.models


class Migration(migrations.Migration):

    dependencies = [
        ('wayfinder', '0004_auto_20161025_1336'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favourites',
            options={},
        ),
        migrations.AlterField(
            model_name='favourites',
            name='picture',
            field=models.ImageField(blank=True, upload_to=wayfinder.models.storeImagePath),
        ),
    ]
