# Generated by Django 4.2.5 on 2023-10-10 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mkpa_app', '0002_orderdetail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='stripe_payment_intent',
            field=models.CharField(max_length=100),
        ),
    ]