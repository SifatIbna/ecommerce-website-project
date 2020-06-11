from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

User = settings.AUTH_USER_MODEL

class BillingProfile(models.Model):
    user             = models.OneToOneField(User,null=True, blank=True, on_delete=models.DO_NOTHING)
    email            = models.EmailField()
    active           = models.BooleanField(default=True)
    updated          = models.DateTimeField(auto_now=True)
    timestamp        = models.DateTimeField(auto_now_add=True)

    #customer id in stripe or Braintree

    def __str__(self):
        return self.email

''' def billing_proile_created_receiver(sender, instance, created, *args, **kwargs):
    if created:
        print("Send to stripe/ braintree")
        instance.customer_id = newID
        instance.save() '''

def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)

post_save.connect(user_created_receiver, sender=User)
