from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from main.utils import *

class Listener(models.Model):
    user = models.OneToOneField(User)
    post_save.connect(create_auth_client, sender=User)

#--AuthenticationID <string>: PK
#--First Name <string>
#--Last Name <string>
#--Email <string>: PK
#--UserDisplayName <string>: PK
#--UserID <int>: PK
#--SuspensionCount<int>
#--ModeratedCommentDeletionsTotal<int>
#--ReportedCommentsTotal<int>
#--SuspensionDate <date>
#--IsVerified <bool>
#--ExplicitOK<bool>

