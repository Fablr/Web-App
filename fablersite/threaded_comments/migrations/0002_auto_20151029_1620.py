# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('threaded_comments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment_Flag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('flag', models.CharField(max_length=30, verbose_name='flag', db_index=True)),
                ('flag_date', models.DateTimeField(default=None, verbose_name='date')),
                ('comment', models.ForeignKey(verbose_name='comment', to='threaded_comments.Comment', related_name='flags')),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL, related_name='comment_flags')),
            ],
            options={
                'verbose_name_plural': 'comment flags',
                'verbose_name': 'comment flag',
            },
        ),
        migrations.AlterUniqueTogether(
            name='commentflag',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='commentflag',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='commentflag',
            name='user',
        ),
        migrations.DeleteModel(
            name='CommentFlag',
        ),
        migrations.AlterUniqueTogether(
            name='comment_flag',
            unique_together=set([('user', 'comment', 'flag')]),
        ),
    ]
