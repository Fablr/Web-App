# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('podcast', '0005_auto_20150727_1625'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=True)),
                ('podcast', models.ForeignKey(related_name='subscription', to='podcast.Podcast')),
                ('user', models.ForeignKey(related_name='subscription', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
