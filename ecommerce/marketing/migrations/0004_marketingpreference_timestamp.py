# Generated by Django 2.2.11 on 2020-06-27 09:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0003_remove_marketingpreference_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='marketingpreference',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
