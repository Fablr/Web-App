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

class CommentViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentViewSerializer

class CommentFlagViewSet(viewsets.ModelViewSet):
    queryset = Comment_Flag.objects.all()
    serializer_class = CommentFlagSerializer

class VoteFilter(django_filters.FilterSet):
    class Meta:
        model=Vote
        fields = ['voter_user', 'voted_user', 'comment']

class VoteViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    filter_class = VoteFilter

    def create(self, request):
        assert 'comment' in request.data, (
            'Missing required field \'comment\''
        )

        assert 'voted_user' not in request.data, (
            'Field \'voted_user\' is read-only'
        )

        try:
            if 'voter_user' in request.data:
                # TODO limit to admins
                voter_user = User.objects.get(pk=request.data['voter_user'])
            else:
                voter_user = self.request.user
            comment = Comment.objects.get(pk=request.data['comment'])
            instance, created = Vote.objects.get_or_create(comment=comment, voter_user=voter_user, voted_user=comment.user, defaults={'value': 0, 'vote_time': timezone.now()})
            comment.net_vote = comment.net_vote - instance.value
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            value = int(request.data['value'])
            if value == 0:
                comment.save()
                instance.delete()
                op = status.HTTP_200_OK
            else:
                comment.net_vote = comment.net_vote + value
                comment.save()
                self.perform_create(serializer)
                if created:
                    op = status.HTTP_201_CREATED
                else:
                    op = status.HTTP_200_OK
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=op, headers=headers)
        except ObjectDoesNotExist:
            raise Http404
