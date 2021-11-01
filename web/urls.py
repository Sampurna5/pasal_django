from django.urls import path
# from .views import homepage
from .views import HomePageView, ProductDetailView, CategoryProductsView, SearchView, SignUpView
from django.contrib.auth.views import LoginView, LogoutView


app_name = 'web'
urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('product/<slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('category/<slug>/', CategoryProductsView.as_view(), name='category-products'),
    path('search', SearchView.as_view(), name='search'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]
