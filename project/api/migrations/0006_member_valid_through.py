# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-24 16:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20170824_0859'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='valid_through',
            field=models.DateField(blank=True, null=True),
        ),
    ]
