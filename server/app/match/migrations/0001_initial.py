# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2019-11-21 13:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('summoner', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchPerformance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_id', models.CharField(default=0, max_length=255)),
                ('mode', models.CharField(blank=True, max_length=100, null=True)),
                ('game_type', models.CharField(blank=True, max_length=255, null=True)),
                ('lane', models.CharField(blank=True, max_length=10, null=True)),
                ('champ', models.IntegerField(default=0)),
                ('opposing_champ', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField()),
                ('win', models.BooleanField(default=False)),
                ('level', models.IntegerField()),
                ('kills', models.IntegerField()),
                ('deaths', models.IntegerField()),
                ('assists', models.IntegerField()),
                ('gold_earned', models.IntegerField()),
                ('double_kills', models.IntegerField()),
                ('triple_kills', models.IntegerField()),
                ('quadra_kills', models.IntegerField()),
                ('penta_kills', models.IntegerField()),
                ('damage_dealt', models.IntegerField()),
                ('summoner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='summoner.Summoner')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='matchperformance',
            unique_together=set([('match_id', 'summoner')]),
        ),
    ]
