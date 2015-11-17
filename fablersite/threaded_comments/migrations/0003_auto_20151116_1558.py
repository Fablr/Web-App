# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('threaded_comments', '0002_auto_20151029_1620'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={},
        ),
        migrations.RemoveField(
            model_name='comment',
            name='path',
        ),
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.IntegerField(null=True),
        ),
    ]
