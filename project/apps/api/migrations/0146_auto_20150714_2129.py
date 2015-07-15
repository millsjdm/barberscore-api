# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0145_auto_20150714_1939'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestant',
            name='end',
            field=models.DateTimeField(null=True, verbose_name='end', blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='start',
            field=models.DateTimeField(null=True, verbose_name='start', blank=True),
        ),
    ]
