# Generated by Django 4.1.7 on 2023-04-02 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=150)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('des', models.TextField(max_length=500)),
                ('product_stock', models.IntegerField(default=0)),
                ('product_pic', models.FileField(default='pro.jpg', upload_to='product_images')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.seller')),
            ],
        ),
    ]
