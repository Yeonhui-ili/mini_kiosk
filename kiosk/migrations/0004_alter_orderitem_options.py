# Generated by Django 5.0.4 on 2024-04-08 21:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0003_alter_orderitem_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderitem',
            options={'verbose_name': 'order_item', 'verbose_name_plural': 'order_items'},
        ),
    ]
