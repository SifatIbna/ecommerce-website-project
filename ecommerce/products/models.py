import random, os
from django.db import models

# Create your models here.

# Every time change model field run python manage.py makemigrations
# python manage.py migrate

def get_filename_ext(filename):
    base_name = os.path.basename(filename)
    name, ext = os.path.splitext(base_name)
    
    return name, ext

def upload_image_path(instace, filename):
    ''' print(instace)
    print(filename) '''
    new_filename = random.randint(1,23232323)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename,ext = ext)
    
    return "products/{new_filename}/{final_filename}".format(
            new_filename=new_filename,
            final_filename = final_filename,
            )

class Product(models.Model):
    title          = models.CharField(max_length=120)
    description    = models.TextField()
    price          = models.DecimalField(max_digits=19, decimal_places=10, default = 39.99)
    image          = models.ImageField(upload_to=upload_image_path, null=True, blank=True)

    def __str__(self):
        return self.title
    