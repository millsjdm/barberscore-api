# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-17 04:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0105_catalog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='is_parody',
        ),
        migrations.AddField(
            model_name='submission',
            name='arranger',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='submission',
            name='is_medley',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='submission',
            name='is_parody',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='submission',
            name='source',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='submission',
            name='title',
            field=models.CharField(default='foo', max_length=200),
            preserve_default=False,
        ),
    ]
