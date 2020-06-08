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

from products.views import (
    product_list_view, 
    ProductdetailView, 
    product_detail_view,
    ProductFeaturedListView,
    ProductFeaturedDetailView,
    )

from .views import (
    home_page, 
    contact_page,
    login_page, 
    register_page,
    )

urlpatterns = [
    path('bootstrap/',TemplateView.as_view(template_name='bootstrap/example.html')),

    path('', home_page, name = 'home'),
    path('contact/', contact_page,name='contact'),
    path('login/',login_page,name='login'),
    path('register/',register_page,name='register'),
    #path('featured/', ProductFeaturedListView.as_view()),
    #path('featured/<int:pk>/', ProductFeaturedDetailView.as_view()),
    path('products/', include(("products.urls","products"),namespace='products')),
    #path('product-fbv/', product_list_view),
    #path('product/<int:pk>/', ProductdetailView.as_view()),
    #path('product/<slug:slug>/', ProductDetailSlugView.as_view()),
    #path('product-fbv/<int:pk>/', product_detail_view),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
