# Generated by Django 3.2.13 on 2022-09-09 05:25

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import pizza_order.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pizza_order', '0017_order_scheduled_detail_scheduled_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 9, 5, 25, 41, 366836, tzinfo=utc)),
        ),
        # migrations.CreateModel(
        #     name='Scheduled_Order',
        #     fields=[
        #         ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        #         ('order_idd', models.CharField(blank=True, max_length=100)),
        #         ('date', models.DateTimeField()),
        #         ('total_amount', models.IntegerField(default=0)),
        #         ('is_payed', models.BooleanField(default=False)),
        #         ('is_delivered', models.BooleanField(default=False)),
        #         ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pizza_order.address')),
        #         ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pizza_order.shop')),
        #         ('status', models.ForeignKey(default=pizza_order.models.get_default_status, on_delete=django.db.models.deletion.CASCADE, to='pizza_order.status')),
        #         ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
        #     ],
        # ),
    ]