# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-07 00:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0095_remove_chart_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chapter',
            name='date',
        ),
        migrations.RemoveField(
            model_name='chapter',
            name='description',
        ),
        migrations.RemoveField(
            model_name='chapter',
            name='email',
        ),
        migrations.RemoveField(
            model_name='chapter',
            name='facebook',
        ),
        migrations.RemoveField(
            model_name='chapter',
            name='location',
        ),
        migrations.RemoveField(
            model_name='chapter',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='chapter',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='chapter',
            name='picture',
        ),
        migrations.RemoveField(
            model_name='chapter',
            name='twitter',
        ),
        migrations.RemoveField(
            model_name='chapter',
            name='website',
        ),
    ]