# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-07 02:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_auto_20170206_1425'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='convention',
            name='bhs_id',
        ),
        migrations.RemoveField(
            model_name='person',
            name='address1',
        ),
        migrations.RemoveField(
            model_name='person',
            name='address2',
        ),
        migrations.RemoveField(
            model_name='person',
            name='city',
        ),
        migrations.RemoveField(
            model_name='person',
            name='country',
        ),
        migrations.RemoveField(
            model_name='person',
            name='postal_code',
        ),
        migrations.RemoveField(
            model_name='person',
            name='state',
        ),
    ]
