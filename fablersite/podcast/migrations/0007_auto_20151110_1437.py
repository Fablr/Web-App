# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0006_subscription'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='podcast',
            name='explicit',
        ),
        migrations.AlterField(
            model_name='episode',
            name='pubdate',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='podcast',
            field=models.ForeignKey(related_name='subscriptionPodcast', to='podcast.Podcast'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='user',
            field=models.ForeignKey(related_name='subscriptionUser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='subscription',
            unique_together=set([('podcast', 'user')]),
        ),
    ]
