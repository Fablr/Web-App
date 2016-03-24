from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from generic_relations.relations import GenericRelatedField

from podcast.models import Podcast, Episode
from podcast.serializers import PodcastSerializer, EpisodeSerializer
from threaded_comments.models import Comment, Vote, Comment_Flag

class VoteSerializer(serializers.ModelSerializer):
    """
    Vote serializer
    """
    class Meta:
        model = Vote
        fields = ('value', 'comment', 'voter_user', 'voted_user', 'vote_time')

class CommentSerializer(serializers.ModelSerializer):
    """
    Accepts comments that can be returned through CommentThreadSerializer
    """
    path = serializers.IntegerField(required=False)
    class Meta:
        model = Comment
        fields = ('comment', 'path')

    def validate_path(self, value):
        """
        Validate that parent does not have it's own parent value
        """
        if value is not None:
            try:
                parent_comment = Comment.objects.get(pk=value)
            except ObjectDoesNotExist:
                raise serializers.ValidationError("Parent comment does not exist")
            if len(parent_comment.path) is not 1:
                raise serializers.ValidationError("Parent comment already has a parent")
        return value

class CommentThreadSerializer(serializers.ModelSerializer):
    """
    Returns serialized Comment
    """
    user_vote = serializers.SerializerMethodField()
    parent = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ('id', 'comment', 'user', 'submit_date', 'edited_date', 'user_name', 'net_vote', 'user_vote', 'parent', 'is_removed')

    def get_user_vote(self, obj):
        try:
            request = self.context.get('request', None)
            if request is None:
                raise ObjectDoesNotExist
            if request.user.is_authenticated():
                return Vote.objects.get(comment=obj.id, voter_user=request.user).value
        except ObjectDoesNotExist:
            return 0

    def get_parent(self, obj):
        index = len(obj.path) - 2
        if index < 0:
            return None
        return obj.path[index]

class CommentViewSerializer(serializers.ModelSerializer):
    """
    Strictly for the API html view, returns all data about a Comment
    """
    content_object = GenericRelatedField({
        Podcast: PodcastSerializer(),
        Episode: EpisodeSerializer()
    })
    content_type = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'content_type', 'content_object', 'user_name', 'comment', 'submit_date', 'edited_date', 'net_vote', 'user')

    def get_content_type(self, obj):
        return obj.content_type.model

class CommentFlagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment_Flag
