# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-25 16:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_member_is_current'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='is_deceased',
            field=models.BooleanField(default=False),
        ),
    ]
