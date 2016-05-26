# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-20 15:36
from __future__ import unicode_literals

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_auto_20160520_0827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestant',
            name='status',
            field=django_fsm.FSMIntegerField(choices=[(0, b'New'), (10, b'Eligible'), (20, b'Ineligible'), (40, b'District Representative'), (50, b'Qualified'), (60, b'Ranked'), (70, b'Scratched'), (80, b'Disqualified')], default=0),
        ),
    ]