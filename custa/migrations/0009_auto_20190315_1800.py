# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-03-15 18:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custa', '0008_requirement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requirement',
            name='description',
            field=models.CharField(max_length=128),
        ),
    ]
