# Generated by Django 4.2.7 on 2023-12-04 06:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_cart_products'),
    ]

    operations = [
        migrations.DeleteModel(
            name='products',
        ),
    ]
