# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-20 20:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0133_auto_20160220_1224'),
    ]

    operations = [
        migrations.AddField(
            model_name='award',
            name='is_novice',
            field=models.BooleanField(default=False),
        ),
    ]
