# Generated by Django 3.2.8 on 2021-10-27 10:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(upload_to='images')),
                ('price', models.IntegerField()),
                ('discounted_price', models.IntegerField()),
                ('description', models.TextField()),
                ('label', models.CharField(blank=True, choices=[('new', 'New'), ('featured', 'Featured'), ('', 'Default')], max_length=50)),
                ('stock', models.CharField(choices=[('in', 'In Stock'), ('out', 'Out of Stock')], max_length=50)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.category')),
            ],
        ),
    ]
