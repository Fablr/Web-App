# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0014_auto_20151116_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episodereceipt',
            name='currentTime',
            field=models.DurationField(default='0d 0:00:02', blank=True),
        ),
    ]
