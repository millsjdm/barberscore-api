# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-27 21:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0086_auto_20160127_1055'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='score',
            options={'ordering': ('song', 'judge')},
        ),
        migrations.AddField(
            model_name='score',
            name='num',
            field=models.IntegerField(default=0),
        ),
    ]