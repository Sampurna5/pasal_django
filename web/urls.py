from django.urls import path
from .views import HomePageView, ProductDetailView, CategoryProductsView, SearchView, CartView, add_to_cart, delete_cart, CartUpdateView


app_name = 'web'
urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('product/<slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('category/<slug>/', CategoryProductsView.as_view(), name='category-products'),
    path('search/', SearchView.as_view(), name='search'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<int:id>/',  add_to_cart, name='add_to_cart'),
    path('delete-cart/<int:id>/', delete_cart, name='delete_cart'),
    path('cart-update/', CartUpdateView.as_view(), name="cart_update" )

]
