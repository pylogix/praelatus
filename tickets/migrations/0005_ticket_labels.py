# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-11 16:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0001_initial'),
        ('tickets', '0004_auto_20170610_2200'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='labels',
            field=models.ManyToManyField(to='labels.Label'),
        ),
    ]