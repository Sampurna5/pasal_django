from django.contrib import admin
from .models import User, Category, Product, Brand, SliderAd, BannerAd, Cart, Wishlist


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'email'
    )


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'price',
        'discounted_price',
        'stock'
    )
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(SliderAd)
admin.site.register(Brand)
admin.site.register(BannerAd)
admin.site.register(Cart)
admin.site.register(Wishlist)
