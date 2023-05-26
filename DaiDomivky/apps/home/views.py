from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


# Create your views here.


# def index(request):
#     return render(request, 'home/index.html')
#

class Index(View):
    def get(self, request):
        return render(request, 'home/index.html')
