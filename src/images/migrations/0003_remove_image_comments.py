# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-12 20:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_image_album'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='comments',
        ),
    ]
