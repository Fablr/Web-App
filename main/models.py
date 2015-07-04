from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, User
from django.db.models.signals import post_save


from django.conf import settings
from django.contrib.auth import get_user_model


#Custom User profile
#class 





class UserProfile(models.Model):
    user = models.OneToOneField(User)

    birthday = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=60, blank=True)
    state_province = models.CharField(max_length=30, blank=True)   

def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
       profile, created = UserProfile.objects.get_or_create(user=instance)  

post_save.connect(create_user_profile, sender=User, weak=False) 

