# Generated by Django 3.2.13 on 2022-08-10 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_order', '0003_auto_20220809_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='total_amount',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='OrderPizza',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(default=0)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pizza_order.order')),
                ('pizza', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pizza_order.pizza')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='pizza',
            field=models.ManyToManyField(through='pizza_order.OrderPizza', to='pizza_order.Pizza'),
        ),
    ]