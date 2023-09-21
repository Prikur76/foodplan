from django.shortcuts import render
from foods.models import Dish

def index(request):
    dishes = Dish.objects.filter(is_active=True)[:3]
    context = {
        'dishes': dishes
    }
    return render(request, 'shop/index.html', context=context)

def contacts(request):
    return render(request, 'shop/contact.html', context={})


def order(request):
    return render(request, 'shop/order.html', context={})