# Generated by Django 4.2.13 on 2024-06-26 19:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_rename_price_orderitem_unit_price_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'permissions': [('cancel_order', 'Can cancel order')]},
        ),
    ]
