from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import status

from threaded_comments.models import Comment, Vote
from threaded_comments.serializers import CommentSerializer, CommentThreadSerializer

class CommentMixin(object):
    """
    Mixin that adds getting comments for associated model, returns a thread of comments for an object.
    Also posts comments associated with a particular model.
    """
    @detail_route(methods=['get', 'post'])
    def comments(self, request, pk):
        if self.request.method == 'GET':
            ctype = ContentType.objects.get_for_model(self.get_serializer().Meta.model)
            comments = Comment.objects.filter(content_type=ctype, object_pk=pk)
            for comment in comments:
                if comment.is_removed is True:
                    comment.comment = "[Removed]"
                    comment.user_name = "[Removed]"
            serializer = CommentThreadSerializer(comments, many=True, context={'request': self.request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif self.request.method == 'POST':
            serializer = CommentSerializer(data=request.data)
            ctype = ContentType.objects.get_for_model(self.get_serializer().Meta.model)
            if serializer.is_valid():
                if 'parent' in request.data:
                    parent_comment = Comment.objects.get(pk=request.data['parent'], content_type=ctype)
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
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
