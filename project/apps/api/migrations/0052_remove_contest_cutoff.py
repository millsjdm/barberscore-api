# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-01 07:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0051_auto_20160229_2300'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contest',
            name='cutoff',
        ),
    ]