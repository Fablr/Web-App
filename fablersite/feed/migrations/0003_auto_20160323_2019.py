# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-24 03:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0002_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(choices=[('Listened', 'Listened'), ('Subscribed', 'Subscribed'), ('Commented', 'Commented'), ('Followed', 'Followed')], max_length=50),
        ),
    ]
