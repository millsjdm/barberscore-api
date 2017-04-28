# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-28 20:47
from __future__ import unicode_literals

from django.db import migrations, models
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20170428_1346'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chart',
            old_name='arranger_fee',
            new_name='bhs_fee',
        ),
        migrations.RemoveField(
            model_name='chart',
            name='arranger',
        ),
        migrations.AlterField(
            model_name='chart',
            name='arrangers',
            field=models.CharField(default='(Unknown)', max_length=200),
        ),
        migrations.AlterField(
            model_name='chart',
            name='composers',
            field=models.CharField(default='(Unknown)', max_length=200),
        ),
        migrations.AlterField(
            model_name='chart',
            name='holders',
            field=models.CharField(default='(Unknown)', max_length=200),
        ),
        migrations.AlterField(
            model_name='chart',
            name='status',
            field=django_fsm.FSMIntegerField(choices=[(-20, 'Rejected'), (-10, 'Inactive'), (0, 'New'), (10, 'Catalog'), (20, 'Cleared')], default=0),
        ),
    ]