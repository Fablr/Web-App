from django.contrib.contenttypes.models import ContentType
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from threaded_comments.models import Comment
from threaded_comments.serializers import *
from rest_framework import authentication, permissions, mixins, generics, viewsets, status
from django.utils import timezone


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
            serializer = CommentThreadSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            serializer = CommentSerializer(data=request.data)
            ctype = ContentType.objects.get_by_natural_key('podcast', self.get_serializer().Meta.model.__name__.lower())
            if serializer.is_valid():
                comment = serializer.save(user=request.user, user_name=request.user.username, object_pk=pk, content_type=ctype, submit_date=timezone.now(), ip_address=request.META['REMOTE_ADDR'], net_vote=1)
                comment.save()
                vote = Vote(voter_user=request.user, voted_user=request.user, comment=comment, value=1, vote_time=timezone.now())
                vote.save()
                serializer = CommentThreadSerializer(comment)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
