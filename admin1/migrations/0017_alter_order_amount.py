# Generated by Django 4.2.5 on 2024-01-30 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin1', '0016_offer_offer_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='amount',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]