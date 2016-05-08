# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-02 22:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0185_auto_20160429_1919'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='convention',
            name='location',
        ),
        migrations.AlterField(
            model_name='contest',
            name='is_qualifier',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='convention',
            name='kind',
            field=models.IntegerField(blank=True, choices=[(10, b'International'), (20, b'District'), (30, b'Division'), (40, b'District and Division'), (200, b'Division I'), (210, b'Division II'), (220, b'Division III'), (230, b'Division IV'), (240, b'Division V'), (250, b'Arizona Division'), (260, b'NE/NW Divisions'), (270, b'SE/SW Divisions'), (280, b'Division One/Packerland Divisions'), (290, b'Northern Plains Division'), (300, b'10,000 Lakes and Southwest Divisions'), (322, b'Northern Division'), (324, b'Central Division'), (330, b'Southern Division'), (340, b'Sunrise Division'), (342, b'Western Regional'), (344, b'Eastern Regional'), (350, b'NE/NW/SE/SW Divisions')], null=True),
        ),
        migrations.AlterField(
            model_name='convention',
            name='season',
            field=models.IntegerField(choices=[(1, b'International'), (2, b'Midwinter'), (3, b'Fall'), (4, b'Spring'), (9, b'Video')]),
        ),
    ]