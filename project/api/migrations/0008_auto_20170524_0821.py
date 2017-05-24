# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-24 15:21
from __future__ import unicode_literals

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_person_part'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='status',
            field=django_fsm.FSMIntegerField(choices=[(0, 'New'), (10, 'Submitted'), (20, 'Accepted'), (30, 'Rejected'), (40, 'Withdrew'), (50, 'Validated'), (52, 'Scratched'), (55, 'Disqualified'), (57, 'Started'), (60, 'Finished'), (90, 'Published')], default=0),
        ),
    ]
