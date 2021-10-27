from django.urls import path
# from .views import homepage
from .views import HomePageView

app_name = 'web'
urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    # path('', homepage, name='index')
]
