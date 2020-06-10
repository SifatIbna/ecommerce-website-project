from django.shortcuts import render

# Create your views here.

def cart_home(request):
    cart_id = request.session.get("cart_id",None)

    if cart_id is None:
        print('get new cart id')
        request.session['cart_id'] = 12
    else:
        print('Cart ID exists')
        
    # print(request.session)
    # print(dir(request.session))

    # request.session.set_expiry(300) # 5 minutes
    # request.session.session_key

    # key = request.session.session_key
    # print(key)

    # request.session['first_name'] = "Sifat" # SET
    # request.session['user'] = request.user # will show error because in session you can not save objects but
    # request.session['user'] = request.user.username # is okay cause it only saving string
    
    return render(request,"carts/home.html",{})


    #'session_key', 'set_expiry'