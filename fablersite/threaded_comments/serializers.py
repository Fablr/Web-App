from rest_framework import serializers
from django.contrib.auth.models import User, Group
from threaded_comments.models import Comment, Vote, CommentFlag

from django.contrib.contenttypes.models import ContentType
from django.conf import settings

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('value', 'comment')


class CommentThreadSerializer(serializers.ModelSerializer):
    #parent = RecursiveField(allow_null=True, many=True)
    username = serializers.SerializerMethodField()
    uservote = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ('id', 'comment', 'user', 'submit_date', 'username', 'is_removed', 'net_vote', 'uservote')

    def get_username(self, obj):
        return obj.user.username
    
    def get_uservote(self, obj):
        try: 
            return Vote.objects.get(comment=obj.id, voter_user=obj.user).value
        except Vote.DoesNotExist:
            return 0
        

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('comment', )

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

#class EpisodeCommentUpdateSerializer

#class EpisodeVoteSerializer(serializers.ModelSerializer):
    #class Meta:
        #model = 
