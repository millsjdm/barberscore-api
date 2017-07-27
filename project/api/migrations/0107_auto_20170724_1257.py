# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-24 19:57
from __future__ import unicode_literals

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0106_auto_20170724_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convention',
            name='status',
            field=django_fsm.FSMIntegerField(choices=[(0, 'New'), (2, 'Published'), (95, 'Archived')], default=0),
        ),
    ]