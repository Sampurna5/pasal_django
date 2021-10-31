from django.shortcuts import redirect, render
from django.views.generic import View
from .models import LABEL, Category, Product, Brand, BannerAd, SliderAd


class HomePageView(View):
    def get(self, request):
        context = {
            'categories': Category.objects.all(),
            'products': Product.objects.all(),
            'brands': Brand.objects.all(),
            'ad_1': BannerAd.objects.filter(rank=1),
            'ad_2': BannerAd.objects.filter(rank=2),
            'ad_3': BannerAd.objects.filter(rank=3),
            'ad_4': BannerAd.objects.filter(rank=4),
            'slider_ads': SliderAd.objects.all(),
            'new_products': Product.objects.filter(label='new').order_by('?'),
            'featured_products': Product.objects.filter(label='featured'),
            'sale_products': Product.objects.filter(label='sale')
        }
        return render(request, 'web/index.html', context)


# class HomePageView2(generic.TemplateView):
#     template_name = 'web/index.html'


class CategoryProductsView(View):
    def get(self, request, slug):
        category = Category.objects.get(id=slug).name
        context = {
            'category': category,
            'categories': Category.objects.all(),
            'category_products': Product.objects.filter(category=slug),
            'new_products': Product.objects.filter(label='new'),
            'sale_products': Product.objects.filter(label='sale', category=slug)
        }
        print(context['sale_products'])
        return render(request, 'web/category-product-list.html', context)


class ProductDetailView(View):
    def get(self, request, slug):
        category = Product.objects.get(slug=slug).category
        context = {
            'categories': Category.objects.all(),
            'selected_product': Product.objects.filter(slug=slug),
            'category_products': Product.objects.filter(category=category).order_by('?')[:4]
        }
        return render(request, 'web/product-details.html', context)


class SearchView(View):
    def get(self, request):
        if request.method == 'GET':
            search = request.GET['search']
            context = {
                'searched_products': Product.objects.filter(
                    name__icontains=search
                ),
                'categories': Category.objects.all(),
                'sale_products': Product.objects.filter(label='sale').order_by('?')[:3],
            }
        else:
            return redirect('/')

        return render(request, 'web/search-product-list.html', context)
