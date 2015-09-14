# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ThreadedComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('object_pk', models.TextField(verbose_name='object ID')),
                ('comment', models.TextField(verbose_name='comment', max_length=3000)),
                ('submit_date', models.DateTimeField(verbose_name='date/time submitted', default=None)),
                ('ip_address', models.GenericIPAddressField(verbose_name='IP address', blank=True, null=True, unpack_ipv4=True)),
                ('is_public', models.BooleanField(verbose_name='is public', default=True, help_text='Uncheck this box to make the comment effectively disappear from the site.')),
                ('is_removed', models.BooleanField(verbose_name='is removed', default=False, help_text='Check this box if the comment is inappropriate. A "This comment has been removed" message will be displayed instead.')),
                ('tree_path', models.CharField(verbose_name='Tree path', editable=False, max_length=500)),
                ('content_type', models.ForeignKey(verbose_name='content type', related_name='content_type_set_for_threadedcomment', to='contenttypes.ContentType')),
                ('last_child', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, verbose_name='Last child', blank=True, to='threadedcomments.ThreadedComment')),
                ('parent', models.ForeignKey(default=None, null=True, verbose_name='Parent', to='threadedcomments.ThreadedComment', blank=True, related_name='children')),
                ('site', models.ForeignKey(to='sites.Site')),
                ('user', models.ForeignKey(verbose_name='user', related_name='threadedcomment_comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Threaded comment',
                'db_table': 'threadedcomments_comment',
                'verbose_name_plural': 'Threaded comments',
                'ordering': ('tree_path',),
            },
        ),
    ]
