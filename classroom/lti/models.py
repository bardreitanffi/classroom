from django.db import models
import hashlib
from django.contrib.auth.models import User
from lti.ims.utils import InvalidLTIRequestError

# Create your models here.
class LTIProfile(models.Model):
    """User profile model. This profile can be retrieved by calling
    get_profile() on the User model
    """
    
    user = models.OneToOneField(User, null=True)
    roles = models.CharField(max_length=255, blank=True, null=True)
    institution_userid = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.user.username


def get_or_create_lti_user(tool_provider):
    email = tool_provider.get_param('lis_person_contact_email_primary')
    first_name = tool_provider.get_param('lis_person_name_full')
    last_name = tool_provider.get_param('lis_person_name_full')
    userid = tool_provider.get_param('user_id')
    if userid is None:
        raise InvalidLTIRequestError
    if email is None:
        email = "{0}@canvas.lms".format(userid)

    import pdb
    pdb.set_trace()
    lti_username = hashlib.sha256(userid).hexdigest()[0:30]  #will not work for multiple LMSes
    try:
        user = User.objects.get(username=lti_username)

    except User.DoesNotExist:
        print 'creating a new user'
        email = email.rstrip('\x0e')
        user = User.objects.create_user(lti_username, email)
        user.set_unusable_password()

        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name

        LTIProfile.objects.create(user=user, institution_userid=userid)

    except User.MultipleObjectsReturned:
        user = get_object_or_404(User, username=lti_username)

    user.backend = 'account.auth_backends.EmailAuthenticationBackend'
    user.save()
    return user

