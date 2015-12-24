from rest_framework import serializers
from django.contrib.auth.models import User, Group
from rest_framework_recursive.fields import RecursiveField
from feed.models import Following

from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core.exceptions import *
from django.utils.duration import duration_string

class FollowingSerializer(serializers.ModelSerializer):
    follower = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())

    class Meta:
        model = Following
