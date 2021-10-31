from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields.files import ImageField


LABEL = (('new', 'New'),('featured', 'Featured'), ('sale', 'On Sale'), ('', 'Default'))
STOCK = (('in', 'In Stock'), ('out', 'Out of Stock'))


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/products')
    price = models.IntegerField()
    discounted_price = models.IntegerField()
    description = models.TextField()
    label = models.CharField(max_length=50, choices=LABEL, blank=True)
    stock = models.CharField(max_length=50, choices=STOCK)

    def __str__(self):
        return self.name


class SliderAd(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/slider')

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=50)
    image = ImageField(upload_to='images/brands')

    def __str__(self):
        return self.name


class BannerAd(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/bannerad')
    rank = models.IntegerField()

    def __str__(self):
        return self.name
