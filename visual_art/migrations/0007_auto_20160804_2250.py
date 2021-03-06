# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-04 22:50
from __future__ import unicode_literals

from django.db import migrations, models
import visual_art.models


class Migration(migrations.Migration):

    dependencies = [
        ('visual_art', '0006_auto_20160804_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='medium',
            field=models.ImageField(null=True, upload_to=visual_art.models.user_medium_path),
        ),
        migrations.AlterField(
            model_name='image',
            name='small',
            field=models.ImageField(null=True, upload_to=visual_art.models.user_small_path),
        ),
    ]
