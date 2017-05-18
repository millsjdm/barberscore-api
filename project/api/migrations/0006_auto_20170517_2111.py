# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-18 04:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20170517_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.EmailField(blank=True, help_text='\n            The contact email of the resource.', max_length=254, null=True, unique=True),
        ),
    ]
