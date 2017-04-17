# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-08 18:57
from __future__ import unicode_literals

from django.db import migrations


def forwards(apps, schema_editor):
    Contest = apps.get_model("app", "Contest")
    Contestant = apps.get_model("app", "Contestant")
    Appearance = apps.get_model("app", "Appearance")
    Entry = apps.get_model("app", "Entry")
    Song = apps.get_model("app", "Song")

    contests = Contest.objects.exclude(contestprivate__isnull=True)
    for contest in contests:
        contest.champion = contest.contestprivate.champion
        contest.save()

    contestants = Contestant.objects.exclude(contestantprivate__isnull=True)
    for contestant in contestants:
        contestant.rank = contestant.contestantprivate.rank
        contestant.mus_points = contestant.contestantprivate.mus_points
        contestant.prs_points = contestant.contestantprivate.prs_points
        contestant.sng_points = contestant.contestantprivate.sng_points
        contestant.tot_points = contestant.contestantprivate.tot_points
        contestant.mus_score = contestant.contestantprivate.mus_score
        contestant.prs_score = contestant.contestantprivate.prs_score
        contestant.sng_score = contestant.contestantprivate.sng_score
        contestant.tot_score = contestant.contestantprivate.tot_score
        contestant.save()

    appearances = Appearance.objects.exclude(appearanceprivate__isnull=True)
    for appearance in appearances:
        appearance.rank = appearance.appearanceprivate.rank
        appearance.mus_points = appearance.appearanceprivate.mus_points
        appearance.prs_points = appearance.appearanceprivate.prs_points
        appearance.sng_points = appearance.appearanceprivate.sng_points
        appearance.tot_points = appearance.appearanceprivate.tot_points
        appearance.mus_score = appearance.appearanceprivate.mus_score
        appearance.prs_score = appearance.appearanceprivate.prs_score
        appearance.sng_score = appearance.appearanceprivate.sng_score
        appearance.tot_score = appearance.appearanceprivate.tot_score
        appearance.save()

    entries = Entry.objects.exclude(entryprivate__isnull=True)
    for entry in entries:
        entry.rank = entry.entryprivate.rank
        entry.mus_points = entry.entryprivate.mus_points
        entry.prs_points = entry.entryprivate.prs_points
        entry.sng_points = entry.entryprivate.sng_points
        entry.tot_points = entry.entryprivate.tot_points
        entry.mus_score = entry.entryprivate.mus_score
        entry.prs_score = entry.entryprivate.prs_score
        entry.sng_score = entry.entryprivate.sng_score
        entry.tot_score = entry.entryprivate.tot_score
        entry.save()

    songs = Song.objects.exclude(songprivate__isnull=True)
    for song in songs:
        song.rank = song.songprivate.rank
        song.mus_points = song.songprivate.mus_points
        song.prs_points = song.songprivate.prs_points
        song.sng_points = song.songprivate.sng_points
        song.tot_points = song.songprivate.tot_points
        song.mus_score = song.songprivate.mus_score
        song.prs_score = song.songprivate.prs_score
        song.sng_score = song.songprivate.sng_score
        song.tot_score = song.songprivate.tot_score
        song.save()


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_auto_20170410_2138'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]