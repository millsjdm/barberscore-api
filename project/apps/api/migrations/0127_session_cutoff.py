# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-01 16:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0126_auto_20160331_0943'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='cutoff',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]