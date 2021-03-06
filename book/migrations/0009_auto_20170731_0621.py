# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-31 06:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0008_bookreading_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookreading',
            name='status',
            field=models.CharField(choices=[('WO', 'Waiting for owner'), ('CO', 'Confirmed by owner'), ('SP', 'Sent by post'), ('RG', 'Reading'), ('RD', 'Read')], default='WO', max_length=2, verbose_name='Status'),
        ),
    ]
