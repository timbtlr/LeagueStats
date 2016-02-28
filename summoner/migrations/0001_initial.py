# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Summoner',
            fields=[
                ('id', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('level', models.IntegerField(default=1)),
                ('rank', models.CharField(max_length=20, null=True, blank=True)),
            ],
        ),
    ]
