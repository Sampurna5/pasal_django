from django.urls import path
from . import views


app_name = 'web'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='index'),
    path('product/<slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('category/<slug>/', views.CategoryProductsView.as_view(), name='category-products'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('cart/', views.CartView.as_view(), name='cart'),
    # path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('delete-cart/<int:id>/', views.delete_cart, name='delete_cart'),
    path('cart-update/', views.CartUpdateView.as_view(), name='cart_update'),
    path('wishlist/',views.WishListView.as_view(), name='wishlist'),
    path('add-to-wishlist/<int:id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('delete-wishlist/<int:id>', views.delete_wislist, name='delete_wishlist'),
]
