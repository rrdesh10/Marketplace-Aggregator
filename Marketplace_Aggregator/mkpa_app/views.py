from django.shortcuts import render
from .models import Product


def index(request):
    products = Product.objects.all()
    return render(request, 'mkpa_app/index.html', {'products':products})


def detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'mkpa_app/detail.html', {'product':product})