# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-06-19 11:21
from __future__ import unicode_literals

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20180619_0853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='about',
            field=models.TextField(blank=True, null=True, verbose_name='About'),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='avatars/default-avatar.png', null=True, upload_to='avatars', verbose_name='Avatar'),
        ),
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='user',
            name='favourite_author',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Favourite author'),
        ),
        migrations.AlterField(
            model_name='user',
            name='favourite_book',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Favourite book'),
        ),
        migrations.AlterField(
            model_name='user',
            name='novaposhta_number',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Novaposhta department number'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, verbose_name='Phone'),
        ),
        migrations.AlterField(
            model_name='user',
            name='reading_preferences',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Reading preferences'),
        ),
    ]