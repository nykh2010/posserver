# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-09-18 04:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='posdata',
            name='x',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='posdata',
            name='y',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
