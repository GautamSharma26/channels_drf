# Generated by Django 3.2.13 on 2022-08-31 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_order', '0009_auto_20220830_1000'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartpizza',
            name='shop',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='pizza_order.shop'),
            preserve_default=False,
        ),
    ]
