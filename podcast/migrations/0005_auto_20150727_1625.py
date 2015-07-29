# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0004_auto_20150720_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='duration',
            field=models.DurationField(null=True),
        ),
    ]
