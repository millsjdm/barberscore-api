# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-20 22:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='award',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='award',
            unique_together=set([]),
        ),
    ]