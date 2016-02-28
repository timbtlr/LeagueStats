# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0004_match_champ'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='assists',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
