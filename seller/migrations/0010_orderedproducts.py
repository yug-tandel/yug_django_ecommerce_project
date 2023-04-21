# Generated by Django 4.1.7 on 2023-04-19 07:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0009_delete_orderedproducts'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderedProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.FloatField()),
                ('my_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.myorders')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.product')),
            ],
        ),
    ]