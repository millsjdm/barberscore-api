# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-03 15:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0070_auto_20170702_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='appearance',
            name='draw',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
