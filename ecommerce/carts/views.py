from django.http import JsonResponse
from django.shortcuts import render,redirect

# Create your views here.

from django.conf import settings
from orders.models import Order
from .models import Cart
from products.models import Product

from accounts.forms import LoginForm,GuestForm

from addresses.forms import AddressForm
from addresses.models import Address

from billing.models import BillingProfile
from accounts.models import GuestEmail

import stripe

STRIPE_SECRET_KEY = getattr(settings,"STRIPE_SECRET_KEY","sk_test_SLVaxFAeisjg7e6OSOAnzm7o00LqkQWxYC")
STRIPE_PUB_KEY = getattr(settings,"STRIPE_PUB_KEY","pk_test_9pAQ7JPwLjnznK5POcjwbFum00nm9g0F5T")

stripe.api_key = STRIPE_SECRET_KEY



''' def cart_create(user=None):
    cart_obj = Cart.objects.create(user=None)
    print("New Cart Created")
    return cart_obj
 '''

def cart_home(request):
    #del request.session['cart_id']
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request,"carts/home.html",{'cart':cart_obj})



def cart_update(request):

    added = True
    product_id  = request.POST.get('id',None)

    if product_id is not None:
        try:

            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect("cart:home")

        cart_obj, new_obj = Cart.objects.new_or_get(request)

        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            added = False
        else:
            cart_obj.products.add(product_obj)

        #return redirect(product_obj.get_absolute_url())
        request.session['cart_items'] = cart_obj.products.count()

        if request.is_ajax():
            print("Ajax Request")
            json_data = {
                "added" : added,
                "removed" : not added,
                "cartItem":cart_obj.products.count(),
            }
            #print(json_data["cartItemCount"])
            #return  JsonResponse({"message":"Error 404"},status_code = 400)
            return JsonResponse(json_data)
    return redirect("cart:home")


def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)

    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")

    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()


    billing_address_id      = request.session.get("billing_address_id",None)
    shipping_address_id     = request.session.get("shipping_address_id",None)


    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

    address_qs = None
    has_card = None
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)

        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile,cart_obj)

        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]


        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]


        if billing_address_id or shipping_address_id:
            order_obj.save()
        has_card = billing_profile.has_card

    if request.method == "POST" :
        is_done = order_obj.check_done()
        if is_done:
            did_charge, charge_msg = billing_profile.charge(order_obj)
            if did_charge:
                order_obj.mark_paid()
                request.session['cart_items'] = 0
                del request.session['cart_id']
                if not billing_profile.user:
                    billing_profile.set_cards_inactive()
                return redirect("cart:checkout_success")
            else:
                print(charge_msg)
                return redirect("cart:checkout")
        '''
        update order_obj to done, "paid
        del request.session
        '''

    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
        "address_qs": address_qs,
        "has_card": has_card,
        "publish_key": STRIPE_PUB_KEY,
    }


    return render(request,"carts/checkout.html", context)


def checkout_done_view(request):
    return render(request,"carts/checkout_done.html",{})
