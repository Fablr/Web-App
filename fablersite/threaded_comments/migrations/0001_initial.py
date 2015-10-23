# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('object_pk', models.TextField(verbose_name='object ID')),
                ('user_name', models.CharField(verbose_name="user's name", max_length=50)),
                ('comment', models.TextField(verbose_name='comment', max_length=10000)),
                ('submit_date', models.DateTimeField(verbose_name='date/time submitted', default=None)),
                ('edited_date', models.DateTimeField(verbose_name='date/time edited', null=True, default=None, blank=True)),
                ('ip_address', models.GenericIPAddressField(verbose_name='IP address', null=True, blank=True, unpack_ipv4=True)),
                ('is_removed', models.BooleanField(verbose_name='is removed', default=False, help_text='Check this box if the comment is inappropriate. A "This comment has been removed" message will be displayed instead.')),
                ('path', django.contrib.postgres.fields.ArrayField(editable=False, base_field=models.IntegerField(), blank=True, size=None)),
                ('net_vote', models.IntegerField()),
                ('content_type', models.ForeignKey(verbose_name='content type', related_name='content_type_set_for_comment', to='contenttypes.ContentType')),
                ('user', models.ForeignKey(verbose_name='user', related_name='comment_comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('path',),
            },
        ),
        migrations.CreateModel(
            name='CommentFlag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('flag', models.CharField(verbose_name='flag', max_length=30, db_index=True)),
                ('flag_date', models.DateTimeField(verbose_name='date', default=None)),
                ('comment', models.ForeignKey(verbose_name='comment', related_name='flags', to='threaded_comments.Comment')),
                ('user', models.ForeignKey(verbose_name='user', related_name='comment_flags', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'comment flag',
                'verbose_name_plural': 'comment flags',
                'db_table': 'django_comment_flags',
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('vote_time', models.DateTimeField()),
                ('value', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(-1), django.core.validators.MaxValueValidator(1)])),
                ('comment', models.ForeignKey(related_name='commentid', to='threaded_comments.Comment')),
                ('voted_user', models.ForeignKey(verbose_name='voted_user', related_name='voted_user', to=settings.AUTH_USER_MODEL)),
                ('voter_user', models.ForeignKey(verbose_name='voter_user', related_name='voter_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('voter_user', 'comment')]),
        ),
        migrations.AlterUniqueTogether(
            name='commentflag',
            unique_together=set([('user', 'comment', 'flag')]),
        ),
    ]
