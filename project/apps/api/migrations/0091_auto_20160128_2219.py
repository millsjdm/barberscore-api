# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-29 06:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0090_score_is_flagged'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='is_flagged',
            field=models.BooleanField(default=False),
        ),
    ]