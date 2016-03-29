# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='id',
            field=models.CharField(max_length=255, serialize=False, primary_key=True),
        ),
    ]
