# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-09-22 12:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0004_posdata_onlineflag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posdata',
            name='x',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='posdata',
            name='y',
            field=models.FloatField(default=0),
        ),
    ]