from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from feed.models import Event

COMMENT_MAX_LENGTH = getattr(settings, 'COMMENT_MAX_LENGTH', 10000)

class Comment(models.Model):
    """
    A user comment about some object.
    """
    # Content-object field
    content_type = models.ForeignKey(ContentType,
                                     verbose_name=_('content type'),
                                     related_name="content_type_set_for_%(class)s")
    object_pk = models.TextField(_('object ID'))
    content_object = GenericForeignKey(ct_field="content_type", fk_field="object_pk")

    # Who posted this comment? If ``user`` is set then it was an authenticated
    # user; otherwise at least user_name should have been set and the comment
    # was posted by a non-authenticated user.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'),
                             blank=False, null=False, related_name="%(class)s_comments")
    user_name = models.CharField(_("user's name"), max_length=50, blank=False)

    comment = models.TextField(_('comment'), max_length=COMMENT_MAX_LENGTH)

    # Metadata about the comment
    submit_date = models.DateTimeField(_('date/time submitted'), default=None)
    edited_date = models.DateTimeField(_('date/time edited'), default=None, blank=True, null=True)
    ip_address = models.GenericIPAddressField(_('IP address'), unpack_ipv4=True, blank=True, null=True)
    is_removed = models.BooleanField(_('is removed'), default=False,
                                     help_text=_('Check this box if the comment is inappropriate. '
                                                 'A "This comment has been removed" message will '
                                                 'be displayed instead.'))
    path = ArrayField(models.PositiveIntegerField(), editable=False, blank=True, null=False, size=2)
    net_vote = models.IntegerField(blank=False, null=False)

    @transaction.atomic
    def save(self, *args, **kwargs):
        if self.submit_date is None:
            self.submit_date = timezone.now()

        log_event = not self.pk

        super(Comment, self).save(*args, **kwargs)

        if log_event:
            ctype = ContentType.objects.get_for_model(self)
            event = Event.objects.create(user=self.user, event_type='Commmented', content_type=ctype, object_id=self.pk)

    def __str__(self):
        return str(self.pk)

    class Meta(object):
        ordering = ('path', )

class Comment_Flag(models.Model):
    """
    Records a flag on a comment. This is intentionally flexible; right now, a
    flag could be:
        * A "removal suggestion" -- where a user suggests a comment for (potential) removal.
        * A "moderator deletion" -- used when a moderator deletes a comment.
    You can (ab)use this model to add other flags, if needed. However, by
    design users are only allowed to flag a comment with a given flag once;
    if you want rating look elsewhere.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'), related_name="comment_flags")
    comment = models.ForeignKey(Comment, verbose_name=_('comment'), related_name="flags")
    flag = models.CharField(_('flag'), max_length=30, db_index=True)
    flag_date = models.DateTimeField(_('date'), default=None)

    # Constants for flag types
    SUGGEST_REMOVAL = "removal suggestion"
    MODERATOR_DELETION = "moderator deletion"
    MODERATOR_APPROVAL = "moderator approval"

    class Meta:
        unique_together = [('user', 'comment', 'flag')]
        verbose_name = _('comment flag')
        verbose_name_plural = _('comment flags')

    def __str__(self):
        return "%s flag of comment ID %s by %s" % (
            self.flag, self.comment_id, self.user.get_username()
        )

    def save(self, *args, **kwargs):
        if self.flag_date is None:
            self.flag_date = timezone.now()
        super(Comment_Flag, self).save(*args, **kwargs)

class Vote(models.Model):
    comment = models.ForeignKey(Comment, related_name='commentid')
    voter_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('voter_user'), related_name='voter_user')
    voted_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('voted_user'), related_name='voted_user')
    vote_time = models.DateTimeField(null=False, blank=False)
    value = models.SmallIntegerField(validators=[MinValueValidator(-1), MaxValueValidator(1)])
    class Meta:
        unique_together = ("voter_user", "comment")
