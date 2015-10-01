from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from .compat import Comment, CommentManager

from django_comments.models import BaseCommentAbstractModel

PATH_SEPARATOR = getattr(settings, 'COMMENT_PATH_SEPARATOR', '/')
PATH_DIGITS = getattr(settings, 'COMMENT_PATH_DIGITS', 10)

COMMENT_MAX_LENGTH = getattr(settings, 'COMMENT_MAX_LENGTH', 5000)

class ThreadedComment(BaseCommentAbstractModel):

    # Who posted this comment? If ``user`` is set then it was an authenticated
    # user; otherwise at least user_name should have been set and the comment
    # was posted by a non-authenticated user.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'),
                             blank=False, null=False, related_name="%(class)s_comments")
    
    comment = models.TextField(_('comment'), max_length=COMMENT_MAX_LENGTH)
    
    # Metadata about the comment
    submit_date = models.DateTimeField(_('date/time submitted'), default=None)
    ip_address = models.GenericIPAddressField(_('IP address'), unpack_ipv4=True, blank=True, null=True)
    is_public = models.BooleanField(_('is public'), default=True,
                                    help_text=_('Uncheck this box to make the comment effectively '
                                                'disappear from the site.'))
    is_removed = models.BooleanField(_('is removed'), default=False,
                                     help_text=_('Check this box if the comment is inappropriate. '
                                                 'A "This comment has been removed" message will '
                                                 'be displayed instead.'))

    parent = models.ForeignKey('self', null=True, blank=True, default=None, related_name='children', verbose_name=_('Parent'))
    last_child = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_('Last child'))
    tree_path = models.CharField(_('Tree path'), max_length=500, editable=False)

    # net_votes = models.IntegerField(blank=False)

    objects = CommentManager()

    vote_weight = models.IntegerField(blank=False, null=False)

    def _get_name(self):
        return self.userinfo["name"]

    def _set_name(self, val):
        if self.user_id:
            raise AttributeError(_("This comment was posted by an authenticated "
                                   "user and thus the name is read-only."))
        self.user_name = val

    name = property(_get_name, _set_name, doc="The name of the user who posted this comment")

    @property
    def depth(self):
        return len(self.tree_path.split(PATH_SEPARATOR))

    @property
    def root_id(self):
        return int(self.tree_path.split(PATH_SEPARATOR)[0])

    @property
    def root_path(self):
        return ThreadedComment.objects.filter(pk__in=self.tree_path.split(PATH_SEPARATOR)[:-1])

    def save(self, *args, **kwargs):
        skip_tree_path = kwargs.pop('skip_tree_path', False)
        super(ThreadedComment, self).save(*args, **kwargs)
        if skip_tree_path:
            return None

        tree_path = str(self.pk).zfill(PATH_DIGITS)
        if self.parent:
            tree_path = PATH_SEPARATOR.join((self.parent.tree_path, tree_path))

            self.parent.last_child = self
            ThreadedComment.objects.filter(pk=self.parent_id).update(last_child=self.id)

        self.tree_path = tree_path
        ThreadedComment.objects.filter(pk=self.pk).update(tree_path=self.tree_path)

    def delete(self, *args, **kwargs):
        # Fix last child on deletion.
        if self.parent_id:
            try:
                prev_child_id = ThreadedComment.objects \
                                .filter(parent=self.parent_id) \
                                .exclude(pk=self.pk) \
                                .order_by('-submit_date') \
                                .values_list('pk', flat=True)[0]
            except IndexError:
                prev_child_id = None
            ThreadedComment.objects.filter(pk=self.parent_id).update(last_child=prev_child_id)
        super(ThreadedComment, self).delete(*args, **kwargs)

    class Meta(object):
        ordering = ('tree_path',)
        db_table = 'threadedcomments_comment'
        verbose_name = _('Threaded comment')
        verbose_name_plural = _('Threaded comments')
