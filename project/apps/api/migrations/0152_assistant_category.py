# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-14 18:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0151_group_chap_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='assistant',
            name='category',
            field=models.IntegerField(blank=True, choices=[(10, b'ACA'), (20, b'Other')], null=True),
        ),
    ]