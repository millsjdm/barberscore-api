# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-30 06:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0096_auto_20160129_2201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='size',
            field=models.IntegerField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], help_text=b'\n            Size of the judging panel (per category).'),
        ),
    ]