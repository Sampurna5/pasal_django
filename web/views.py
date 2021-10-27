from django.shortcuts import render
from django.views.generic import View
from django.views import generic


# def homepage(request):
#     return render(request, 'web/index.html')


class HomePageView(View):
    def get(self, request):
        return render(request, 'web/index.html')


# class HomePageView2(generic.TemplateView):
#     template_name = 'web/index.html'
