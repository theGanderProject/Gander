# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-07 00:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visual_art', '0011_auto_20160807_0014'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='favorite_count',
            field=models.IntegerField(default=0),
        ),
    ]