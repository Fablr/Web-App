from django_hosts import patterns, host
from django.conf import settings

host_patterns = patterns(
    '',
    host('www', settings.ROOT_URLCONF, name='www'),
    host('(?!www)\w+', 'fablersite.urls', name='site'),
)
