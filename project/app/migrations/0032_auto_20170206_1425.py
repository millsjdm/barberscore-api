# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-06 22:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_auto_20170206_1238'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='convention',
            name='chorus_prelims',
        ),
        migrations.RemoveField(
            model_name='convention',
            name='entity',
        ),
        migrations.RemoveField(
            model_name='convention',
            name='is_prelims',
        ),
        migrations.RemoveField(
            model_name='convention',
            name='quartet_prelims',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='source',
        ),
    ]
