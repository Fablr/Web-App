# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0009_auto_20151110_1900'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='episode',
            name='explicit',
        ),
        migrations.AlterField(
            model_name='episode',
            name='pubdate',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2015, 11, 11, 6, 28, 41, 9861, tzinfo=utc)),
        ),
    ]
