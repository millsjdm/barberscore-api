# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-31 16:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_office_is_rep'),
    ]

    operations = [
        migrations.AddField(
            model_name='office',
            name='is_ca',
            field=models.BooleanField(default=False),
        ),
    ]