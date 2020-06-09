>>> from tags.models import Tag
>>> Tag.objects()
>>> Tag.objects.all()
>>> Tag.objects.last()
<Tag: blue>
>>> black =  Tag.objects.last()
>>> black.title
'blue'
>>> black.slug
'blue'
>>> black.active
True
>>> black.products
<django.db.models.fields.related_descriptors.create_forward_many_to_many_manager.<locals>.ManyRelatedManager object at 0x7f925e88df98>
>>> black.products.all()
<ProductQuerySet [<Product: shirt>, <Product: Jeans>, <Product: pants>]>
>>> exit()
 
 
>>> from products.models import Product
>>> qs = Product.objects.all()
>>> qs
<ProductQuerySet [<Product: V-neck>, <Product: Jeans>, <Product: shirt>, <Product: pants>]>
>>> neck = qs.first()

>>> neck
<Product: shirt>
>>> neck.title
'shirt'
>>> neck.description
'New Shirt'

>>> tshirt.tag_set.all()
>>> neck.tag_set.all()
<QuerySet [<Tag: T-shirt>, <Tag: T-shirt>, <Tag: red>, <Tag: blue>]>
>>> neck.tag_set.filter(title__iexact='red')
<QuerySet [<Tag: red>]>

