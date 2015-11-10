# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0007_auto_20151110_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='podcast',
            name='explicit',
            field=models.BooleanField(default=False),
        ),
    ]
