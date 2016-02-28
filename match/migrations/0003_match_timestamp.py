# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0002_auto_20160226_0402'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='timestamp',
            field=models.DateTimeField(default=None),
            preserve_default=False,
        ),
    ]
