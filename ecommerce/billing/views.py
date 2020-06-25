from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.utils.http import is_safe_url
# Create your views here.
import stripe
stripe.api_key = "sk_test_SLVaxFAeisjg7e6OSOAnzm7o00LqkQWxYC"
STRIPE_PUB_KEY = "pk_test_9pAQ7JPwLjnznK5POcjwbFum00nm9g0F5T"

def payment_method_view(request):
    next_url = None

    next_post = request.GET.get('next')

    if is_safe_url(next_post, request.get_host()):
        next_url = next_post

    return render(request,'billing/payment-method.html',{"publish_key": STRIPE_PUB_KEY, "next_url" : next_url})

def payment_method_createview(request):
    if request.method == "POST" and request.is_ajax():
        print(request.POST)
        return JsonResponse({"message":"Done"})
    return HttpResponse("error", status_code=401)
