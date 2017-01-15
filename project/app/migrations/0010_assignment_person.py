# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-15 13:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_session_panel_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assignments', to='app.Person'),
        ),
    ]
