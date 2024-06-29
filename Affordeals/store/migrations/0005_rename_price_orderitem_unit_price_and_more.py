# Generated by Django 4.2.13 on 2024-06-26 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_order_rename_user_id_address_siteuser_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='price',
            new_name='unit_price',
        ),
        migrations.RenameField(
            model_name='products',
            old_name='price',
            new_name='unit_price',
        ),
        migrations.AlterField(
            model_name='products',
            name='image',
            field=models.ImageField(blank=True, help_text='Upload an image file (optional)', null=True, upload_to='images/'),
        ),
    ]