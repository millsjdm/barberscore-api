# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-24 18:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_member_valid_through'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='is_current',
            field=models.BooleanField(default=False),
        ),
    ]
