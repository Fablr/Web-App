from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    birthday = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=60, blank=True)
    state_province = models.CharField(max_length=30, blank=True)   

    def create_user_profile(sender, instance=None, created=False, **kwargs):  
        if created:  
           profile, created = UserProfile.objects.get_or_create(user=instance) 
    
    def delete_user_profile(sender, instance=None, **kwargs):  
        if instance:  
            user_profile = UserProfile.objects.get(user=instance)
            user_profile.delete()

    post_save.connect(create_user_profile, sender=User, weak=False) 
    pre_delete.connect(delete_user_profile, sender=User, weak=False)
