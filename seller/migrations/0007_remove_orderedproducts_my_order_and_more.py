# Generated by Django 4.1.7 on 2023-04-17 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0006_orderedproducts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderedproducts',
            name='my_order',
        ),
        migrations.RemoveField(
            model_name='orderedproducts',
            name='product',
        ),
        migrations.DeleteModel(
            name='MyOrders',
        ),
        migrations.DeleteModel(
            name='OrderedProducts',
        ),
    ]
