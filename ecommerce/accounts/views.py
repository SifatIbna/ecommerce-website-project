
from django.http import HttpResponse
from django.views.generic import CreateView, FormView
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.utils.http import is_safe_url

from .signals import user_logged_in_signal
from .forms import LoginForm, RegisterForm,GuestForm
from .models import GuestEmail

# Create your views here.

def guest_login_page(request):
    form = GuestForm(request.POST or None)

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

        email = form.cleaned_data.get("email")

        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id 

        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("/register")
    # Redirect to a success page.
        
    else:
    # Return an 'invalid login' error message.
        print("Error")
        return redirect("/home")

    return redirect("/register")


class LoginView(FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'accounts/login.html'

    def form_valid(self,form):
        request = self.request
        next_post = request.POST.get('next')
        next_ = request.GET.get('next')
        redirect_path = next_ or next_post or None

        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        user = authenticate(request, username=email, password=password)
        if user is not None:
            #print(redirect_path)
            login(request, user)
            user_logged_in_signal.send(user.__class__,instance=user,request=request)
            try:
                del request.session['guest_email_id']
            except:
                pass

            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        return super(LoginView,self).form_invalid(form)

def login_page(request):
    form = LoginForm(request.POST or None)

    context = {
        "form" : form
    }

    ''' print(request.POST)
    print(request.GET) '''
    
    next_post = request.POST.get('next')
    next_ = request.GET.get('next')
    redirect_path = next_ or next_post or None

    ''' print(next_) '''
    #print(next_post)

    if form.is_valid():
        print(form.cleaned_data)
        context['form'] = form

        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            #print(redirect_path)
            login(request, user)
            
            try:
                del request.session['guest_email_id']
            except:
                pass

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

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/login/'

''' User = get_user_model()

def register_page(request):
    form = RegisterForm(request.POST or None)

    context = {
        "form":form
    }

    if form.is_valid():
        form.save()
        
    return render(request,"accounts/register.html",context)
 '''
