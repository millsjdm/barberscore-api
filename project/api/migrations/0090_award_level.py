# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-13 05:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0089_auto_20170711_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='award',
            name='level',
            field=models.IntegerField(blank=True, choices=[(10, 'Championship'), (20, 'Award'), (30, 'Qualifier')], null=True),
        ),
    ]
