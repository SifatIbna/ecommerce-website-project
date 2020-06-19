from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.db.models.signals import pre_save,post_save

from accounts.signals import user_logged_in_signal

from .signals import object_viewed_signal
from .utils import get_client_ip

User = settings.AUTH_USER_MODEL

FORCE_SESSION_TO_ONE = getattr(settings, 'FORCE_SESSION_TO_ONE', False)
FORCE_INACTIVE_USER_END_SESSION = getattr(settings,'FORCE_INACTIVE_USER_END_SESSION',False)


class ObjectViewed(models.Model):
    user                = models.ForeignKey(User, blank = True, null = True, on_delete=models.DO_NOTHING)
    ip_address           = models.CharField(max_length=200, blank=True, null=True)
    content_type        = models.ForeignKey(ContentType,on_delete=models.DO_NOTHING)
    object_id           = models.PositiveIntegerField()
    content_object      = GenericForeignKey('content_type','object_id')
    timestamp           = models.DateTimeField(auto_now_add=True)

    '''

        --- content_type field contains all kinds of models
        --- object_id field contains id of that content_type

        --- content_object is basically combination of content_type and object_id ,
            As one of these fields is ForeignKey , That's why we are using 
            GenericForeignKey

    '''

    def __str__(self):
        return "%s viewed %s" %(self.content_object, self.timestamp)

    class Meta:
        ordering                = ['-timestamp']
        verbose_name            = 'Object viewed'
        verbose_name_plural     = 'Objects viewed'

def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    c_type          = ContentType.objects.get_for_model(sender)
    ''' print(sender)
    print(instance)
    print(request)
    print(request.user) '''

    new_view_obj = ObjectViewed.objects.create(
                    user        = request.user,
                    content_type = c_type,
                    object_id   = instance.id,
                    ip_address  = get_client_ip(request),                
        )

object_viewed_signal.connect(object_viewed_receiver)




class UserSession(models.Model):
    user                = models.ForeignKey(User, blank = True, null = True, on_delete=models.DO_NOTHING)
    ip_address           = models.CharField(max_length=200, blank=True, null=True)
    session_key         = models.CharField(max_length=200, blank=True, null=True)
    timestamp           = models.DateTimeField(auto_now_add=True)
    active              = models.BooleanField(default=True)
    ended               = models.BooleanField(default=False)

    def end_session(self):
        session_key = self.session_key
        
        try:
            Session.objects.get(pk=session_key).delete()
            self.ended = True
            self.active = False
            self.save()
        except:
            pass
        return self.ended

def post_save_session_receiver(sender, instance,created,*args, **kwargs):
    if created:
        qs = UserSession.objects.filter(user=instance.user, ended=False, active=False).exclude(id=instance.id)
        for i in qs:
            i.end_session()
    if not instance.active and not instance.ended:
        instance.end_session()

if FORCE_SESSION_TO_ONE :
    post_save.connect(post_save_session_receiver,sender=UserSession)

def post_save_user_change_receiver(sender, instance, created, *args, **kwargs):
    if not created:
        if instance.active == False:
            qs = UserSession.objects.filter(user=instance.user, ended=False, active=False).exclude(id=instance.id)
            for i in qs:
                i.end_session()
                
if FORCE_INACTIVE_USER_END_SESSION:
    post_save.connect(post_save_user_change_receiver,sender=User)

def user_logged_in_receiver(sender, instance, request, *args, **kwargs):
    print(instance)

    ip_address = get_client_ip(request)
    user = instance
    session_key = request.session.session_key
    UserSession.objects.create(
        user=user,
        ip_address=ip_address,
        session_key=session_key
    )

user_logged_in_signal.connect(user_logged_in_receiver)