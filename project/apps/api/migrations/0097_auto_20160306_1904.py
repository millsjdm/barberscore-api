# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-07 03:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0096_auto_20160306_1649'),
    ]

    operations = [
        migrations.RenameField(
            model_name='judge',
            old_name='panel_id',
            new_name='bhs_panel_id',
        ),
        migrations.RemoveField(
            model_name='contest',
            name='parent',
        ),
        migrations.AlterField(
            model_name='chapter',
            name='name',
            field=models.CharField(help_text=b'\n            The name of the resource.', max_length=200, unique=True),
        ),
    ]