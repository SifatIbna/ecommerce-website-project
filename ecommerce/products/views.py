from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import Http404
from django.shortcuts import render, get_object_or_404

from .models import Product
from analytics.mixins import ObjectViewedMixin
from carts.models import Cart

# Create your views here.

class ProductFeaturedListView(ListView):
    template_name       = "products/list.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all().featured()

class ProductFeaturedDetailView(ObjectViewedMixin,DetailView):
    queryset            = Product.objects.all().featured()
    template_name       = "products/featured-detail.html"

    ''' def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.featured()
 '''
class ProductListView(ListView):
    queryset            = Product.objects.all()
    template_name       = "products/list.html"

    ''' def get_context_data(self, *args,**kwargs):
        context = super(ProductListView,self).get_context_data(*args,**kwargs)
        print(context)

        return context '''

    def get_context_data(self,*args,**kwargs):
        context = super(ProductListView,self).get_context_data(*args,**kwargs)
        context["cart"], new_obj = Cart.objects.new_or_get(self.request)
        #print(context["cart"])
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all()
    

def product_list_view(request):
    queryset               = Product.objects.all()
    context                = {
        'object_list': queryset
    }   
    return render(request,"products/list.html", context)

class ProductDetailSlugView(ObjectViewedMixin,DetailView):
    queryset            = Product.objects.all()
    template_name       = "products/detail.html"

    def get_context_data(self,*args,**kwargs):
        context = super(ProductDetailSlugView,self).get_context_data(*args,**kwargs)
        context["cart"], new_obj = Cart.objects.new_or_get(self.request)
        #print(context["cart"])
        return context
    
    def get_object(self,*args,**kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        #instance = Product.objects.get_by_id(pk)
        ''' if instance is None:
            raise Http404("Product doesn't exist") '''
        try:
            instance = Product.objects.get(slug=slug, active = True)
        except Product.DoesNotExist:
            raise Http404("Not Found")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active = True)
            instance = qs.first()
        except:
            raise Http404("BLEH")
        
        return instance

class ProductdetailView(ObjectViewedMixin,DetailView):
    #queryset            = Product.objects.all()
    template_name       = "products/detail.html"

    def get_context_data(self, *args,**kwargs):
        context = super(ProductdetailView,self).get_context_data(*args,**kwargs)
        print(context)

        return context

    def get_object(self,*args,**kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Product doesn't exist")
        return instance

    ''' def get_queryset(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        return Product.objects.filter(pk=pk) '''

def product_detail_view(request, pk=None, *args, **kwargs):
    '''     instance               = Product.objects.get(pk=pk)
    #instance                = get_object_or_404(Product,pk=pk)
    print(instance)
    qs = Product.objects.filter(id=pk)

    if qs.exists() and qs.count() == 1:
        instance = qs.first()
    else:
        raise Http404("Product doesn't exists")
    '''
    instance = Product.objects.get_by_id(pk)
    if instance is None:
        raise Http404("Product doesn't exist")

    context                = {
        'object': instance
    }   
    return render(request,"products/detail.html", context)
