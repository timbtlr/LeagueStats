# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2019-09-24 15:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0004_match_match_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='id',
            field=models.CharField(auto_created=True, max_length=255, primary_key=True, serialize=False),
        ),
    ]