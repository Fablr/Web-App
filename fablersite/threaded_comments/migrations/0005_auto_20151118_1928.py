# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('threaded_comments', '0004_auto_20151116_1619'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('path',)},
        ),
        migrations.RemoveField(
            model_name='comment',
            name='parent',
        ),
        migrations.AddField(
            model_name='comment',
            name='path',
            field=django.contrib.postgres.fields.ArrayField(editable=False, size=2, blank=True, base_field=models.PositiveIntegerField(), default=[0]),
            preserve_default=False,
        ),
    ]
