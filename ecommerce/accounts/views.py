
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.utils.http import is_safe_url

from .forms import LoginForm, RegisterForm


# Create your views here.

def login_page(request):
    form = LoginForm(request.POST or None)

    context = {
        "form" : form
    }

    print(request.POST)
    print(request.GET)
    
    next_post = request.POST.get('next')
    next_ = request.GET.get('next')
    redirect_path = next_ or next_post

    print(next_)
    #print(next_post)

    if form.is_valid():
        print(form.cleaned_data)
        context['form'] = form

        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            print(redirect_path)
            login(request, user)
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        # Redirect to a success page.
            
        else:
        # Return an 'invalid login' error message.
            print("Error")
            return redirect("/home")

    return render(request,"accounts/login.html",context)

User = get_user_model()

def register_page(request):
    form = RegisterForm(request.POST or None)

    context = {
        "form":form
    }

    if form.is_valid():
        print(form.cleaned_data)

        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")

        new_user=User.objects.create_user(username, email,password)
        print(new_user)
        
    return render(request,"accounts/register.html",context)

