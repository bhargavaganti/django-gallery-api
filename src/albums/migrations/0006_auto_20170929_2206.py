# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-29 22:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0005_auto_20170929_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='images',
            field=models.ManyToManyField(blank=True, related_name='album_images', to='images.Image'),
        ),
    ]
