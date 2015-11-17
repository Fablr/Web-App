# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0015_auto_20151116_2139'),
    ]

    operations = [
        migrations.RenameField(
            model_name='episodereceipt',
            old_name='currentTime',
            new_name='mark',
        ),
    ]
