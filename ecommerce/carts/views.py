from django.shortcuts import render

# Create your views here.
from .models import Cart

''' def cart_create(user=None):
    cart_obj = Cart.objects.create(user=None)
    print("New Cart Created")
    return cart_obj
 '''

def cart_home(request):
    #del request.session['cart_id']
    cart_obj = Cart.objects.new_or_get(request)
    
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

    return render(request,"carts/home.html",{}) 


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