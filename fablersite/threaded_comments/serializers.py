from rest_framework import serializers
from django.contrib.auth.models import User, Group
from threaded_comments.models import Comment, Vote, Comment_Flag

from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core.exceptions import *

class VoteSerializer(serializers.ModelSerializer):
    """
    Vote serializer 
    """
    class Meta:
        model = Vote
        fields = ('value', 'comment')

class CommentSerializer(serializers.ModelSerializer):
    """
    Accepts comments that can be returned through CommentThreadSerializer
    """
    parent = serializers.IntegerField(required=False)
    class Meta:
        model = Comment
        fields = ('comment', 'parent')

    def validate_parent(self, value):
        """
        Validate that parent does not have it's own parent value
        """
        if value is not None:
            try: 
                parent_comment = Comment.objects.get(pk=value)
            except ObjectDoesNotExist:
                raise serializers.ValidationError("Parent comment does not exist")
            if parent_comment.parent is not None:
                raise serializers.ValidationError("Parent comment already has a parent")
        return value


class CommentThreadSerializer(serializers.ModelSerializer):
    """
    Returns serialized Comment
    """
    uservote = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ('id', 'comment', 'user', 'submit_date', 'user_name', 'is_removed', 'net_vote', 'uservote', 'parent')

    def get_uservote(self, obj):
        try: 
            return Vote.objects.get(comment=obj.id, voter_user=obj.user).value
        except Vote.DoesNotExist:
            return 0

class CommentViewSerializer(serializers.ModelSerializer):
    """
    Strictly for the API html view, returns all data about a Comment
    """
    class Meta:
        model = Comment

class CommentFlagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment_Flag
