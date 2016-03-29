# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0003_match_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='champ',
            field=models.IntegerField(default=0),
        ),
    ]
