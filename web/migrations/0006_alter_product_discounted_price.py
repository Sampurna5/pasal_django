# Generated by Django 3.2.8 on 2021-10-31 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_auto_20211029_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discounted_price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
