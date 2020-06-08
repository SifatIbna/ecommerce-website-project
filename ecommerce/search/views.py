from django.shortcuts import render
from django.views.generic.list import ListView

from products.models import Product
# Create your views here.

class SearchProductView(ListView):
    queryset            = Product.objects.all()
    template_name       = "products/list.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        print(request.GET)

        query = request.GET.get('q',None)

        if query is not None:
            return Product.objects.filter(title__icontains=query)
        return Product.objects.features()


        '''
            __icontains = fields contains this
            __iexact = fields exactly contains this
        '''