from django.conf import settings

from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from django.utils.http import is_safe_url

from .models import BillingProfile,Card

import stripe

STRIPE_SECRET_KEY = getattr(settings,"STRIPE_SECRET_KEY","sk_test_SLVaxFAeisjg7e6OSOAnzm7o00LqkQWxYC")
STRIPE_PUB_KEY = getattr(settings,"STRIPE_PUB_KEY","pk_test_9pAQ7JPwLjnznK5POcjwbFum00nm9g0F5T")

stripe.api_key = STRIPE_SECRET_KEY

def payment_method_view(request):

    # if request.user.is_authenticated():
    #     billing_profile = request.user.billing_profile
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if not billing_profile:
        return redirect("/cart")

    next_url = None

    next_post = request.GET.get('next')

    print(next_post)

    if is_safe_url(next_post, request.get_host()):
        next_url = next_post

    return render(request,'billing/payment-method.html',{"publish_key": STRIPE_PUB_KEY, "next_url" : next_url})


def payment_method_createview(request):
    if request.method == "POST" and request.is_ajax():
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if not  billing_profile:
            return HttpResponse({"message":"Sorry! Can not find this user!"}, status_code=401)
        token = request.POST.get("token")
        if token is not None:

            new_card_obj = Card.objects.add_new(billing_profile,token)

        return JsonResponse({"message":"Success! Your Card was added"})
    return HttpResponse("error", status_code=401)
