# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-03 14:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0128_round_datetm'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='round',
            name='date',
        ),
    ]