# Generated by Django 3.2.6 on 2021-08-22 03:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_orderitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=20)),
                ('postalcode', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=20)),
                ('shipping_price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('order', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.order')),
            ],
        ),
    ]