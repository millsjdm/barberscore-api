# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0064_auto_20151227_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convention',
            name='status',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (10, b'Built'), (20, b'Started'), (30, b'Finished'), (50, b'Final')]),
        ),
    ]