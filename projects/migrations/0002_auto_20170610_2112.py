# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-10 21:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'permissions': (('admin_project', 'Ability to admin the project.'), ('view_project', 'Ability to view the project.'), ('create_content', 'Ability to create content within the project.'), ('edit_content', 'Ability to edit content within the project.'), ('comment_content', 'Ability to comment on content within the project.'))},
        ),
    ]