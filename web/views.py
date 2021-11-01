from django.shortcuts import redirect, render, reverse
from django.contrib import messages, auth
from django.views.generic import View
from django.views import generic
from .models import LABEL, Category, Product, Brand, BannerAd, SliderAd
from .forms import CustomUserCreationForm


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


class SignUpView(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse('web:login')

# def signup(request):
#     if request.method=='POST':
#         first_name = request.POST['firstname']
#         last_name = request.POST['lastname']
#         phone = request.POST['phone']
#         email = request.POST['email']
#         password = request.POST['password']
#         re_password = request.POST['re_password']

#         if password == re_password:
#             for character in first_name:
#                 if character.isdigit():
#                     messages.error(request, 'Name cannot have number!!')
#                     return redirect("web:signup")
#             for character in last_name:
#                 if character.isdigit():
#                     messages.error(request, 'Name cannot have number!!')
#                     return redirect("web:signup")
#             if len(password) < 8:
#                 messages.error(request, 'Password length must exceed 8 characters!!')
#                 return redirect("web:signup")
#            elif User.objects.filter(username=username).exists():
#                messages.error(request, 'Username already exists!!')
#                return redirect('web:signup')
#             elif User.objects.filter(email=email).exists():
#                 messages.error(request, 'Email already registered!!')
#                 return redirect('web:signup')
#             else:
#                 customer = user.objects.create(
#                     first_name=first_name,
#                     last_name=last_name,
#                     phone = phone,
#                     email=email,
#                     password=password
#                 )
#                 customer.save()

#                 messages.success(request, 'Account created successfully!!')
#                 return redirect('web:signup')
#         else:
#             messages.error(request, 'Password does not match!!')    
#     return render(request, 'web/signup.html')


# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']

#         user = auth.authenticate(username=username, password=password)
#         if user is not None:
#             auth.login(request, user)
#             return redirect('/')
#         else:
#             messages.error(request, 'Invalid email/username or password!!')
#             return redirect('web:login')
