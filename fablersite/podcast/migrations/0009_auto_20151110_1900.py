# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0008_podcast_explicit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='duration',
            field=models.DurationField(default='0d 0:00:02', blank=True),
        ),
        migrations.AlterField(
            model_name='episode',
            name='pubdate',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 11, 3, 0, 41, 725576, tzinfo=utc), blank=True),
        ),
    ]
