# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255)),
                ('link', models.URLField(max_length=255, unique=True)),
                ('subtitle', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True, max_length=4000)),
                ('blocked', models.BooleanField(default=False)),
                ('pubdate', models.DateTimeField(null=True)),
                ('duration', models.CharField(blank=True, max_length=255)),
                ('keywords', models.CharField(blank=True, max_length=100)),
                ('explicit', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Podcast',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255)),
                ('author', models.CharField(blank=True, max_length=255)),
                ('summary', models.TextField(blank=True, max_length=4000)),
                ('category', models.CharField(blank=True, max_length=255)),
                ('explicit', models.CharField(blank=True, max_length=255)),
                ('link', models.URLField(blank=True, max_length=255)),
                ('language', models.CharField(blank=True, max_length=255)),
                ('copyright', models.CharField(blank=True, max_length=255)),
                ('blocked', models.BooleanField(default=False)),
                ('complete', models.BooleanField(default=False)),
                ('keywords', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(blank=True, max_length=255, unique=True)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='podcast',
            name='publisher',
            field=models.ForeignKey(to='podcast.Publisher'),
        ),
        migrations.AddField(
            model_name='episode',
            name='podcast',
            field=models.ForeignKey(to='podcast.Podcast'),
        ),
    ]
