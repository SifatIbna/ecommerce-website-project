from django.shortcuts import render

# Create your views here.
import stripe
stripe.api_key = "sk_test_SLVaxFAeisjg7e6OSOAnzm7o00LqkQWxYC"
STRIPE_PUB_KEY = "pk_test_9pAQ7JPwLjnznK5POcjwbFum00nm9g0F5T"

def payment_method_view(request):
    if request.method == "POST":
        print(request.POST)
    return render(request,'billing/payment-method.html',{"publish_key": STRIPE_PUB_KEY})
