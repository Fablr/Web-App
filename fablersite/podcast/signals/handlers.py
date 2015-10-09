from django.dispatch import receiver
from django_comments.models import Comment
from django_comments.signals import comment_was_posted
from django.db.models.signals import post_save

@receiver(comment_was_posted)
def vote_creation(sender, comment, request, **kwargs):
    print("Trying to save vote")
    vote = Vote(user=request.user, comment=comment, value=1)
    vote.save()
    pass

@receiver(post_save, sender=Comment)
def my_handler(sender, **kwargs):
    print("hi I'm a handler")
    pass

