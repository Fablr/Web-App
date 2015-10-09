# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('podcast', '0006_vote'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='user',
        ),
        migrations.AddField(
            model_name='vote',
            name='vote_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 1, 0, 28, 59, 527310, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vote',
            name='voted_user',
            field=models.ForeignKey(related_name='voted_user', default=14, verbose_name='voted_user', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vote',
            name='voter_user',
            field=models.ForeignKey(related_name='voter_user', default=14, verbose_name='voter_user', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
