# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-12 18:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workflows', '0003_auto_20170610_2320'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebHook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('url', models.TextField()),
                ('method', models.CharField(max_length=10)),
                ('body', models.TextField()),
            ],
        ),
        migrations.RenameField(
            model_name='status',
            old_name='color',
            new_name='bg_color',
        ),
        migrations.AddField(
            model_name='status',
            name='state',
            field=models.CharField(default='TODO', max_length=11),
        ),
        migrations.AlterField(
            model_name='transition',
            name='workflow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transitions', to='workflows.Workflow'),
        ),
    ]