# Generated by Django 3.2.6 on 2021-09-05 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_variant_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='variant',
            name='variant_id',
            field=models.PositiveIntegerField(null=True, unique=True),
        ),
    ]
