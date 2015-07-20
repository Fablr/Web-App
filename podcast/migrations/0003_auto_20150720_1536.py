# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0002_auto_20150712_1958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='podcast',
            field=models.ForeignKey(to='podcast.Podcast', related_name='episode'),
        ),
        migrations.AlterField(
            model_name='podcast',
            name='publisher',
            field=models.ForeignKey(to='podcast.Publisher', related_name='podcast'),
        ),
        migrations.AlterField(
            model_name='publisher',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]
