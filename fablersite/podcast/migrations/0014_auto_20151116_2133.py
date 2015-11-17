# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0013_auto_20151116_2041'),
    ]

    operations = [
        migrations.RenameField(
            model_name='episodereceipt',
            old_name='time',
            new_name='currentTime',
        ),
    ]
