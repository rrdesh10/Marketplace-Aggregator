# Generated by Django 4.2.5 on 2023-10-13 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mkpa_app', '0004_product_seller'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='total_sales',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='total_sales_amount',
            field=models.IntegerField(default=0),
        ),
    ]
