from django.shortcuts import render,redirect

# Create your views here.

from orders.models import Order
from .models import Cart
from products.models import Product
from accounts.forms import LoginForm,GuestForm
from billing.models import BillingProfile
from accounts.models import GuestEmail

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
    # print("Here")
    print(request.POST)

    product_id  = request.POST.get('id',None)
    print(product_id)
    if product_id is not None:
        try:
            print("here")
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect("cart:home")

        cart_obj, new_obj = Cart.objects.new_or_get(request)

        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
        else:
            cart_obj.products.add(product_obj)

        #return redirect(product_obj.get_absolute_url())
        request.session['cart_items'] = cart_obj.products.count()
    return redirect("cart:home")   


def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    #print(cart_obj.products.count())
    print(cart_obj)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")
    
    login_form = LoginForm()
    guest_form = GuestForm()
    billing_profile, billing_profile_created = BillingProfile.objects.now_or_get(request)
    
    if billing_profile is not None:
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile,cart_obj)
    
    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
    }
    return render(request,"carts/checkout.html", context)