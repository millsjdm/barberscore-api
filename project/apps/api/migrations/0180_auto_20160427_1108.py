# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-27 18:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0179_organization_representative'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convention',
            name='venue',
            field=models.ForeignKey(blank=True, help_text=b'\n            The venue for the convention.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='conventions', to='api.Venue'),
        ),
    ]