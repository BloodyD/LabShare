# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-04 12:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labshare', '0012_gpuprocess'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='cpu_util',
            field=models.FloatField(default=0),
        ),
    ]
