# Generated by Django 2.2.11 on 2020-06-04 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=10, default=39.99, max_digits=19),
        ),
    ]
