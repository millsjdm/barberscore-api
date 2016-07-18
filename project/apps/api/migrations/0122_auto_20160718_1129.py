# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-18 18:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import mptt.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0121_auto_20160718_0958'),
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(editable=False, max_length=255, unique=True)),
                ('status', models.IntegerField(choices=[(0, b'New'), (10, b'Active'), (20, b'Inactive')], default=0)),
                ('convention', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hosts', to='api.Convention')),
                ('organization', mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hosts', to='api.Organization')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='host',
            unique_together=set([('convention', 'organization')]),
        ),
    ]
