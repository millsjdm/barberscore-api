# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-08 16:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0136_remove_convention_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='convention',
            old_name='datet',
            new_name='date',
        ),
    ]