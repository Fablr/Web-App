# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0010_auto_20151110_2228'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='explicit',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='episode',
            name='pubdate',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 11, 6, 29, 53, 102032, tzinfo=utc), blank=True),
        ),
    ]
