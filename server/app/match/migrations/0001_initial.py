# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summoner', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.CharField(primary_key=True, max_length=255, serialize=False)),
                ('champ', models.IntegerField(default=0)),
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
                ('summoner', models.ForeignKey(to='summoner.Summoner')),
            ],
        ),
    ]
