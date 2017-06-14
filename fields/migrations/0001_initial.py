# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-14 21:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('data_type', models.CharField(choices=[('FLOAT', 'FLOAT'), ('STRING', 'STRING'), ('TEXT', 'TEXT'), ('INTEGER', 'INTEGER'), ('DATE', 'DATE'), ('OPTION', 'OPTION')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='FieldOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='FieldValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('int_value', models.IntegerField(null=True)),
                ('str_value', models.CharField(max_length=255, null=True)),
                ('opt_value', models.CharField(max_length=255, null=True)),
                ('flt_value', models.FloatField(null=True)),
                ('date_value', models.DateTimeField(null=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fields.Field')),
            ],
        ),
        migrations.AddField(
            model_name='field',
            name='options',
            field=models.ManyToManyField(blank=True, null=True, to='fields.FieldOption'),
        ),
    ]
