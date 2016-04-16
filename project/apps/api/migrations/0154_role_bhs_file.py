# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-15 23:14
from __future__ import unicode_literals

import apps.api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0153_role_bhs_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='bhs_file',
            field=models.FileField(blank=True, null=True, upload_to=apps.api.models.generate_image_filename),
        ),
    ]