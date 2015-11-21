from django.contrib.contenttypes.models import ContentType
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from threaded_comments.models import Comment
from threaded_comments.serializers import *
from rest_framework import authentication, permissions, mixins, generics, viewsets, status
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

class CommentMixin(object):
    """
    Mixin that adds getting comments for associated model, returns a thread of comments for an object.
    Also posts comments associated with a particular model.
    """
    @detail_route(methods=['get', 'post'])
    def comments(self, request, pk):
        if self.request.method == 'GET':
            # Access class name of the class we're serializing (podcast, episode, publisher, etc.)
            # For some reason, it has to be in lower case to find the ContentType, which is why there's a .lower()
            ctype = ContentType.objects.get_by_natural_key('podcast', self.get_serializer().Meta.model.__name__.lower())
            comments = Comment.objects.filter(content_type=ctype, object_pk=pk)
            for comment in comments:
                if comment.is_removed is True:
                    comment.comment = "Has been removed"
                    comment.user_name = "[Removed]"
            serializer = CommentThreadSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif self.request.method == 'POST':
            serializer = CommentSerializer(data=request.data)
            ctype = ContentType.objects.get_by_natural_key('podcast', self.get_serializer().Meta.model.__name__.lower())
            if serializer.is_valid():
                if('path' in request.data):
                    parent_comment = Comment.objects.get(pk=request.data['path'], content_type=ctype)
                    comment = serializer.save(user=request.user, user_name=request.user.username, object_pk=pk, content_type=ctype, submit_date=timezone.now(), ip_address=request.META['REMOTE_ADDR'], net_vote=1, path=parent_comment.path)
                    comment.path.append(comment.id)
                else:
                    comment = serializer.save(user=request.user, user_name=request.user.username, object_pk=pk, content_type=ctype, submit_date=timezone.now(), ip_address=request.META['REMOTE_ADDR'], net_vote=1, path=[0, ])
                    comment.path = [comment.id, ]
                comment.save()
                vote = Vote(voter_user=request.user, voted_user=request.user, comment=comment, value=1, vote_time=timezone.now())
                vote.save()
                serializer = CommentThreadSerializer(comment)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # NEED PERMISSIONS HERE
        # elif self.request.method == 'DELETE':
        #    comment = Comment.objects.get(pk=pk)
        #    comment.is_removed = True
        #    return Response()


