# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('podcast', '0012_auto_20151115_1518'),
    ]

    operations = [
        migrations.CreateModel(
            name='EpisodeReceipt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DurationField()),
                ('completed', models.BooleanField(default=False)),
                ('episode', models.ForeignKey(related_name='receiptEpisode', to='podcast.Episode')),
                ('user', models.ForeignKey(related_name='receiptUser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='episodereceipt',
            unique_together=set([('episode', 'user')]),
        ),
    ]
