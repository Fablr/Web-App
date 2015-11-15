# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0011_auto_20151110_2229'),
    ]

    operations = [
        migrations.AddField(
            model_name='podcast',
            name='image',
            field=models.URLField(default='', max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='publisher',
            name='image',
            field=models.URLField(default='', max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='episode',
            name='pubdate',
            field=models.DateTimeField(default=django.utils.timezone.now, blank=True),
        ),
    ]
