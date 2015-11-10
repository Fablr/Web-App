from rest_framework import serializers
from django.contrib.auth.models import User, Group
from threaded_comments.models import Comment, Vote, Comment_Flag

from django.contrib.contenttypes.models import ContentType
from django.conf import settings

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('value', 'comment')


class CommentThreadSerializer(serializers.ModelSerializer):
    #parent = RecursiveField(allow_null=True, many=True)
    uservote = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ('id', 'comment', 'user', 'submit_date', 'user_name', 'is_removed', 'net_vote', 'uservote', 'path')

    def get_uservote(self, obj):
        try: 
            return Vote.objects.get(comment=obj.id, voter_user=obj.user).value
        except Vote.DoesNotExist:
            return 0
        

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('comment', )

class CommentFlagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment_Flag
