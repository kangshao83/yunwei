# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-03 02:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hosts',
            options={'ordering': ['-hostip']},
        ),
        migrations.AddField(
            model_name='groups',
            name='actionbackup',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='hosts',
            name='actionbackup',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
