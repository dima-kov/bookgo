# Generated by Django 2.0.7 on 2018-12-26 21:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0002_auto_20181226_2100'),
        ('book', '0021_auto_20180621_1308'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='club',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='club.Club', verbose_name='Club'),
            preserve_default=False,
        ),
    ]
