# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-05 14:07
from __future__ import unicode_literals

from django.db import migrations


def forward(apps, schema_editor):
    Assignment = apps.get_model("app", "Assignment")
    items = Assignment.objects.filter(person=None)
    for i in items:
        i.delete()


def reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20170203_1038'),
    ]

    operations = [
        migrations.RunPython(forward, reverse)
    ]