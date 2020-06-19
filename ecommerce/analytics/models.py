from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = settings.AUTH_USER_MODEL

class ObjectViewed(models.Model):
    user                = models.ForeignKey(User, blank = True, null = True, on_delete=models.DO_NOTHING)
    ip_addess           = models.CharField(max_length=200, blank=True, null=True)
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
