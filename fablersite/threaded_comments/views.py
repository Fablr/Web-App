from django.utils import timezone
import django_filters
from django.http import Http404
from django.contrib.contenttypes.models import ContentType


from threaded_comments.models import Comment, Comment_Flag, Vote
from threaded_comments.serializers import *
from authentication.permissions import IsStaffOrTargetUser

from podcast.models import Podcast, Episode, Publisher

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, mixins, generics, viewsets, status

class CommentViewSet(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentViewSerializer

class CommentFlagViewSet(viewsets.ModelViewSet):
    queryset = Comment_Flag.objects.all()
    serializer_class = CommentFlagSerializer 

class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Using episode id, update comment's vote weight 
            comment_id = Comment.objects.get(pk=request.data['comment'])
            # If vote already exists update existing vote to reflect new value
            try: 
                vote = Vote.objects.get(comment=comment_id, voter_user=request.user)
                comment_id.net_vote = comment_id.net_vote - vote.value
                vote.value = int(request.data['value'])
                if vote.value == 0:
                    vote.delete()
                else:
                    vote.save()
            except Vote.DoesNotExist:
                vote = serializer.save(voter_user=request.user, voted_user=comment_id.user, vote_time=timezone.now())
            comment_id.net_vote = comment_id.net_vote + int(request.data['value'])
            comment_id.save()            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

