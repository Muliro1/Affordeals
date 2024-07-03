# Generated by Django 4.2.13 on 2024-06-30 22:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_rename_order_shoppingorder_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppingorderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='items', to='store.shoppingorder'),
        ),
    ]