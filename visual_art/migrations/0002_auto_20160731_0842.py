# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-31 08:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visual_art', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='path',
        ),
        migrations.AddField(
            model_name='image',
            name='original',
            field=models.ImageField(default='', upload_to=''),
            preserve_default=False,
        ),
    ]
