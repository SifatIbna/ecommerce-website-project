from django.conf import settings
from django.shortcuts import render,redirect
from django.views.generic import UpdateView,View
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse

from .forms import MarketingPreferenceForm
from .models import MarketingPreference
from .utils import MailChimp
from .mixins import CsrfExemptMixin

class MarketingPreferenceUpdateView(SuccessMessageMixin,UpdateView):
    form_class = MarketingPreferenceForm
    template_name = 'base/forms.html'
    success_url = '/settings/email/'
    success_message = "Your Preferences have been updated"

    def dispatch(self,*args,**kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect("/login/?next=/settings/email/")
        return super(MarketingPreferenceUpdateView,self).dispatch(*args,**kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(MarketingPreferenceUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Update Email Preferences'
        return context

    def get_object(self):
        user = self.request.user
        obj, created  =MarketingPreference.objects.get_or_create(user = user)
        return obj



class MailChimpWebhookView(CsrfExemptMixin, View):
    def get(self,request,*args,**kwargs):
        return HttpResponse("Thank You", status=200)

    def post(self,request,*args,**kwargs):
        data = request.POST
        list_id = data.get('data[list_id]')
        if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID) :
            hook_type = data.get("type")

            email = data.get('data[email]')
            response_status, response = MailChimp().check_subscription_status(email)
            sub_status = response['status']
            is_subbed = None
            mailchimp_subbed = None
            if sub_status == 'subscribed' :
                is_subbed, mailchimp_subbed = (True,True)
            elif sub_status == 'unsubscribed' :
                is_subbed, mailchimp_subbed = (False,False)
            if is_subbed is not None and mailchimp_subbed is not None:
                qs = MarketingPreference.objects.filter(user__email__iexact=email)
                if qs.exists():
                    qs.update(
                            subscribed = is_subbed,
                            mailchimp_subscribed = mailchimp_subbed,
                            mailchimp_msg = str(data)
                    )
            return HttpResponse("Thank You", status=200)

# def mailchimp_webhook_view(request):
#     data = request.POST
#     list_id = data.get('data[list_id]')
#     if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID) :
#         hook_type = data.get("type")
#
#         email = data.get('data[email]')
#         response_status, response = MailChimp().check_subscription_status(email)
#         sub_status = response['status']
#         is_subbed = None
#         mailchimp_subbed = None
#         if sub_status == 'subscribed' :
#             is_subbed, mailchimp_subbed = (True,True)
#         elif sub_status == 'unsubscribed' :
#             is_subbed, mailchimp_subbed = (False,False)
#         if is_subbed is not None and mailchimp_subbed is not None:
#             qs = MarketingPreference.objects.filter(user__email__iexact=email)
#             if qs.exists():
#                 qs.update(
#                         subscribed = is_subbed,
#                         mailchimp_subscribed = mailchimp_subbed,
#                         mailchimp_msg = str(data)
#                 )
#         return HttpResponse("Thank You", status=200)
