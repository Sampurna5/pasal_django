from django.db.models.aggregates import Sum
from django.db.models.expressions import F
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, reverse
from django.contrib import messages, auth
from django.views.generic import View
from django.views import generic
from .models import Category, Product, Brand, BannerAd, SliderAd, User, Cart, Wishlist
from .forms import CustomUserCreationForm
from django.core.paginator import Paginator

def cartOperations(request):
    cart_obj = Cart.objects.filter(user=request.user.username)
    wishlist_obj = Wishlist.objects.filter(user=request.user.username)

    if cart_obj.exists():
        cart_total = cart_obj.values("subtotal").aggregate(total=Sum("subtotal"))
        cart_count = cart_obj.values("quantity").aggregate(total=Sum("quantity"))
    else:
        cart_total = {'total': 0}
        cart_count = {'total': 0}

    wishlist_count = wishlist_obj.all().count()
    # select sum(subtotal) as total from Cart 
    
    return {
        'cart_total':cart_total, 
        'cart_count':cart_count,
        'wishlist_count': wishlist_count,
        }


class HomePageView(View):
    def get(self, request):
        # user = request.user.username
        # cart = Cart.objects.filter(user=user)
        # cart_total = 0
        # cart_quantity = 0
        # for item in cart:
        #     cart_total += item.subtotal
        #     cart_quantity += item.quantity
        cartData = cartOperations(request)

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
            'sale_products': Product.objects.filter(label='sale'),
            'cart_total': cartData['cart_total'],
            'cart_count': cartData['cart_count'],
            'wishlist_count': cartData['wishlist_count'],
        }
        print(cartData)
        return render(request, 'web/index.html', context)


# class HomePageView2(generic.TemplateView):
#     template_name = 'web/index.html'


class CategoryProductsView(View):
    def get(self, request, slug):
        # Pagination
        p = Paginator(Product.objects.filter(category=slug), 6)
        page = request.GET.get('page')
        products = p.get_page(page)

        category = Category.objects.get(id=slug).name

        cartData = cartOperations(request)

        context = {
            'category': category,
            'categories': Category.objects.all(),
            # 'category_products': Product.objects.filter(category=slug),
            'category_products': products,
            'new_products': Product.objects.filter(label='new'),
            'sale_products': Product.objects.filter(label='sale', category=slug),
            'cart_total': cartData['cart_total'],
            'cart_count': cartData['cart_count'],
            'wishlist_count': cartData['wishlist_count'],
        }
        print(context['sale_products'])
        return render(request, 'web/category-product-list.html', context)


class ProductDetailView(View):
    def get(self, request, slug):
        category = Product.objects.get(slug=slug).category

        cartData = cartOperations(request)

        context = {
            'categories': Category.objects.all(),
            'selected_product': Product.objects.filter(slug=slug),
            'category_products': Product.objects.filter(category=category).order_by('?')[:4],
            'cart_total': cartData['cart_total'],
            'cart_count': cartData['cart_count'],
            'wishlist_count': cartData['wishlist_count'],
        }
        return render(request, 'web/product-details.html', context)


class SearchView(View):
    def get(self, request):        
        search = request.GET['search']

        # Pagination
        p = Paginator(Product.objects.filter(name__icontains=search), 6)
        page = request.GET.get('page')
        products = p.get_page(page)

        cartData = cartOperations(request)

        context = {
            'searched_products': products,
            'categories': Category.objects.all(),
            'sale_products': Product.objects.filter(label='sale').order_by('?')[:3],
            'cart_total': cartData['cart_total'],
            'cart_count': cartData['cart_count'],
            'wishlist_count': cartData['wishlist_count'],
        }

        return render(request, 'web/search-product-list.html', context)


class SignUpView(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse('web:login')


class CartView(View):
    def get(self, request):
        user = request.user.username

        # cart = Cart.objects.filter(user=user)
        # total = 0
        # for item in cart:
        #     total += item.subtotal
        
        cartData = cartOperations(request)

        context = {
            'categories': Category.objects.all(),
            'cart_items': Cart.objects.filter(user=user),
            'cart_total': cartData['cart_total'],
            'cart_count': cartData['cart_count'],
            'wishlist_count': cartData['wishlist_count'],
        }
    
        return render(request, 'web/shopping-cart.html', context)


def add_to_cart(request, id):
    user = request.user.username
    if Cart.objects.filter(product=id, user=user).exists():
        quantity = Cart.objects.get(product=id, user=user).quantity
        quantity += 1
        # cart_total = Cart.objects.get(product=id, user=user).total

        if Product.objects.get(id=id).discounted_price:
            product_unit_price = Product.objects.get(id=id).discounted_price
            product_total = product_unit_price * quantity
        else:
            product_unit_price = Product.objects.get(id=id).price
            product_total = product_unit_price * quantity

        # cart_total += product_total

        Cart.objects.filter(product=id, user=user).update(
            quantity=quantity,
            subtotal=product_total,
            )

    else:
        # cart_total = Cart.objects.all()[0].total

        if Product.objects.get(id=id).discounted_price:
            product_total = Product.objects.get(id=id).discounted_price
        else:
            product_total = Product.objects.get(id=id).price

        # cart_total += product_total

        cart = Cart.objects.create(
            product = Product.objects.get(id=id),
            user = user,
            subtotal = product_total,
            # total = cart_total,
        )
        cart.save()

    return redirect('web:cart')


def delete_cart(request, id):
    user = request.user.username
    Cart.objects.filter(product=id, user=user).delete()

    return redirect('web:cart')

class CartUpdateView(View):
    def get(self, request):
        product_id = self.request.GET.get("id")
        operation = self.request.GET.get("operation")
        user = request.user.username
        product_obj = Product.objects.get(id=product_id)
        cart_obj = Cart.objects.get(product=product_obj, user=user)
        if operation == "increase":
            cart_obj.quantity += 1
            cart_obj.subtotal += product_obj.price
        else:
            cart_obj.quantity -= 1
            cart_obj.subtotal -= product_obj.price

        if product_obj.discounted_price:
            product_unit_price = product_obj.discounted_price
            product_total = product_unit_price * cart_obj.quantity
        else:
            product_unit_price = product_obj.price
            product_total = product_unit_price * cart_obj.quantity

        # cart_obj.update(
        #     quantity=cart_obj.quantity,
        #     subtotal=product_total,
        #     )
        cart_obj.save()
        data = {
            'product_id': product_id,
            'subtotal': cart_obj.subtotal,
            'cart_count': cart_obj.quantity
        }
        print(cart_obj.quantity)
        return JsonResponse(data)


class WishListView(View):
    def get(self, request):
        user = request.user.username

        cartData = cartOperations(request)

        context = {
            'wishlist_items': Wishlist.objects.filter(user=user),
            'cart_total': cartData['cart_total'],
            'cart_count': cartData['cart_count'],
            'wishlist_count': cartData['wishlist_count'],
            'categories': Category.objects.all(),
        }

        return render(request, 'web/wishlist.html', context)


def add_to_wishlist(request, id):
    user = request.user.username

    if Wishlist.objects.filter(product=id, user=user).exists():
        pass
    else:
        # if Product.objects.get(id=id).discounted_price:
        #     product_total = Product.objects.get(id=id).discounted_price
        # else:
        #     product_total = Product.objects.get(id=id).price

        wishlist = Wishlist.objects.create(
            product = Product.objects.get(id=id),
            user = user,
        )
        wishlist.save()

    return redirect('web:wishlist')


def delete_wislist(request, id):
    user = request.user.username
    Wishlist.objects.filter(product=id, user=user).delete()

    return redirect('web:wishlist')

# def increase_in_cart(request, id):
#     user = request.user.username
#     quantity = Cart.objects.get(product=id, user=user).quantity
#     quantity += 1

#     if Product.objects.get(id=id).discounted_price:
#         product_unit_price = Product.objects.get(id=id).discounted_price
#         product_total = product_unit_price * quantity
#     else:
#         product_unit_price = Product.objects.get(id=id).price
#         product_total = product_unit_price * quantity

#     Cart.objects.filter(product=id, user=user).update(
#         quantity=quantity,
#         subtotal=product_total,
#         )

#     return redirect('web:cart')


# def decrease_in_cart(request, id):
#     user = request.user.username
#     quantity = Cart.objects.get(product=id, user=user).quantity
#     quantity -= 1

#     if Product.objects.get(id=id).discounted_price:
#         product_unit_price = Product.objects.get(id=id).discounted_price
#         product_total = product_unit_price * quantity
#     else:
#         product_unit_price = Product.objects.get(id=id).price
#         product_total = product_unit_price * quantity

#     Cart.objects.filter(product=id, user=user).update(
#         quantity=quantity,
#         subtotal=product_total,
#         )

#     return redirect('web:cart')


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
