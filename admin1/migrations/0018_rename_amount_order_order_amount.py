# Generated by Django 4.2.5 on 2024-01-30 06:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin1', '0017_alter_order_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='amount',
            new_name='order_amount',
        ),
    ]
