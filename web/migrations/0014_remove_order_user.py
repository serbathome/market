# Generated by Django 4.0.6 on 2022-07-10 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0013_order_delete_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
    ]
