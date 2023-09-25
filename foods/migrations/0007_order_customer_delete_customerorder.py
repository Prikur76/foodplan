# Generated by Django 4.2.5 on 2023-09-25 11:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
        ('foods', '0006_order_yookassa_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='customers.customer', verbose_name='клиент'),
        ),
        migrations.DeleteModel(
            name='CustomerOrder',
        ),
    ]
