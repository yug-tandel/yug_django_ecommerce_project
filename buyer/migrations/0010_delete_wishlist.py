# Generated by Django 4.1.7 on 2023-04-09 17:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buyer', '0009_alter_wishlist_product_cart'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Wishlist',
        ),
    ]
