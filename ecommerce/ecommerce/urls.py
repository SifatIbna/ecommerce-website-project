"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

from addresses.views import checkout_address_create_view,checkout_address_reuse_view

from billing.views import payment_method_view

from products.views import (
    product_list_view, 
    ProductdetailView, 
    product_detail_view,
    ProductFeaturedListView,
    ProductFeaturedDetailView,
    )

from accounts.views import LoginView,RegisterView,guest_login_page

from .views import (
    home_page, 
    contact_page,
    )

urlpatterns = [
    path('bootstrap/',TemplateView.as_view(template_name='bootstrap/example.html')),

    path('', home_page, name = 'home'),
    path('contact/', contact_page,name='contact'),

    path('login/',LoginView.as_view(),name='login'),
    path('login/guest/',guest_login_page,name='guest_login'),

    path('logout/',LogoutView.as_view(),name='logout'),
    
    path('register/',RegisterView.as_view(),name='register'),
    path('product/', include(("products.urls","products"),namespace='products')),
    path('search/', include(("search.urls","search"),namespace='search')),

  
    path('admin/', admin.site.urls),

    #path('cart/',cart_home,name='cart'),
    path('cart/', include(("carts.urls","carts"),namespace='cart')),
    path('checkout/address/create/',checkout_address_create_view,name='checkout_address_create'),
    path('checkout/address/reuse/',checkout_address_reuse_view,name='checkout_address_reuse'),

    path('billing/payment-method', payment_method_view,name='billing-payment-method'),


]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
