# Generated by Django 3.2.13 on 2022-08-08 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_order', '0002_auto_20220808_1014'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='total_amount',
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]
