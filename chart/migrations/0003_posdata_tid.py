# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-09-19 08:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0002_auto_20180918_1252'),
    ]

    operations = [
        migrations.AddField(
            model_name='posdata',
            name='tid',
            field=models.CharField(default=django.utils.timezone.now, max_length=30),
            preserve_default=False,
        ),
    ]