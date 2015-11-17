# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('threaded_comments', '0003_auto_20151116_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
