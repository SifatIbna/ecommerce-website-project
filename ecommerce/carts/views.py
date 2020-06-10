from django.shortcuts import render,redirect

# Create your views here.
from .models import Cart
from products.models import Product

''' def cart_create(user=None):
    cart_obj = Cart.objects.create(user=None)
    print("New Cart Created")
    return cart_obj
 '''

def cart_home(request):
    #del request.session['cart_id']
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request,"carts/home.html",{'cart':cart_obj}) 

    ''' products = cart_obj.products.all()
    total = 0

    for x in products:
        total += x.price

    print(total) '''

    ''' cart_id = request.session.get("cart_id",None)

    if cart_id is None:
        cart_obj = cart_create()
        request.session['cart_id'] = cart_obj.id 
        
    else:

    qs = Cart.objects.filter(id=cart_id)
    if qs.count() == 1:
        cart_obj = qs.first()
        
        if request.user.is_authenticated and cart_obj.user is None:
            cart_obj.user = request.user
            cart_obj.save()

        #redundant if cases, cause we did it in models.py

    else:
        cart_obj = Cart.objects.new(user=request.user)
        request.session['cart_id'] = cart_obj.id '''

    


    # print(request.session)
    # print(dir(request.session))

    # request.session.set_expiry(300) # 5 minutes
    # request.session.session_key

    # key = request.session.session_key
    # print(key)

    # request.session['first_name'] = "Sifat" # SET
    # request.session['user'] = request.user # will show error because in session you can not save objects but
    # request.session['user'] = request.user.username # is okay cause it only saving string

    


    #'session_key', 'set_expiry'


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