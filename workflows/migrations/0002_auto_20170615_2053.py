# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-15 20:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workflows', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transition',
            name='from_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='workflows.Status'),
        ),
    ]