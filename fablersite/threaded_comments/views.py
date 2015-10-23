from django.utils import timezone
import django_filters
from django.http import Http404
from django.contrib.contenttypes.models import ContentType


from threaded_comments.models import Comment, CommentFlag, Vote
from threaded_comments.serializers import *
from authentication.permissions import IsStaffOrTargetUser

from podcast.models import Podcast, Episode, Publisher

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, mixins, generics, status

 class VoteDetail(APIView):
     def post(self, request, format=None):
         serializer = VoteSerializer(data=request.data)
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
 
class ThreadList(APIView):
    def get_object(self, pk):
        try: 
            return Comment.objects.all()
        except Comment.DoesNotExist:
            raise Http404
    def get(self, request, object_type, object_id, format=None):
        try:
            ctype = ContentType.objects.get_by_natural_key('podcast', object_type)
        except ContentType.DoesNotExist:
            raise Http404("ContentType " + object_type + " does not exist")
        
        comments = Comment.objects.filter(content_type=ctype, object_pk=object_id)
        serializer = CommentThreadSerializer(comments, many=True)
        return Response(serializer.data)


class CommentsDetail(APIView):
    def post(self, request, object_type, object_id, parent_id=None, format=None):
        serializer = CommentSerializer(data=request.data)
        try:
            ctype = ContentType.objects.get_by_natural_key('podcast', object_type)
        except ContentType.DoesNotExist:
            raise Http404("ContentType " + object_type + " does not exist")

        if serializer.is_valid():
            # Create a comment, then create a corresponding vote
            if parent_id is None:
                comment = serializer.save(user=request.user, user_name=request.user.username, object_pk=object_id, content_type=ctype, 
                        submit_date=timezone.now(), ip_address=request.META['REMOTE_ADDR'], net_vote=1, path=[-1, ])
                comment.path = [comment.id, ]
            else:
                # Check to see if parentid is valid
                try: 
                    parent_comment = Comment.objects.get(pk=parent_id, content_type=ctype)
                except Comment.DoesNotExist:
                    raise Http404("Parent comment id does not exist")
                # Otherwise create comment using parent comment's path
                comment = serializer.save(user=request.user, user_name=request.user.username, object_pk=object_id, content_type=ctype, 
                        submit_date=timezone.now(), ip_address=request.META['REMOTE_ADDR'], net_vote=1, path=parent_comment.path)
                comment.path.append(comment.id)
            comment.save()
            vote = Vote(voter_user=request.user, voted_user=request.user, comment=comment, value=1, vote_time=timezone.now())
            vote.save()
            serializer = CommentThreadSerializer(comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #def delete(self, request, pk):
    #    comment = Comment.objects.get(pk=pk)
    #    comment.delete()
    #    queryset = Vote.objects.filter(comment_id=pk)
    #    queryset.delete()
    #    return Response(status=status.HTTP_204_NO_CONTENT)

    #def update(self, request, pk):
        #comment = 
