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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('win', models.BooleanField(default=False)),
                ('level', models.IntegerField()),
                ('kills', models.IntegerField()),
                ('deaths', models.IntegerField()),
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
