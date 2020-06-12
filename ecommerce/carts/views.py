from django.shortcuts import render,redirect

# Create your views here.

from orders.models import Order
from .models import Cart
from products.models import Product
from accounts.forms import LoginForm
from billing.models import BillingProfile

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
    print("Here")
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
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")
    else:
        order_obj, new_obj = Order.objects.get_or_create(cart=cart_obj)

    user = request.user
    billing_profile = None
    login_form = LoginForm()

    if user.is_authenticated:
        billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(
                                                    user=user, 
                                                    email=user.email)
    
    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
    }
    return render(request,"carts/checkout.html", context)