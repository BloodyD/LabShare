# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-17 13:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('labshare', '0011_gpu_in_use'),
    ]

    operations = [
        migrations.CreateModel(
            name='GPUProcess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process', models.CharField(max_length=511)),
                ('pid', models.PositiveIntegerField()),
                ('memory_usage', models.CharField(max_length=100)),
                ('gpu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='processes', to='labshare.GPU')),
            ],
        ),
    ]
