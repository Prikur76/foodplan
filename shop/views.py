from django.shortcuts import render
from foods.models import Dish, FoodIntolerance

def index(request):
    dishes = Dish.objects.filter(is_active=True)[:3]
    context = {
        'dishes': dishes
    }
    return render(request, 'shop/index.html', context=context)

def contacts(request):
    return render(request, 'shop/contact.html', context={})


def order(request):
    foods_intolerances = FoodIntolerance.objects.all()
    print(request.GET)
    return render(request, 'shop/order.html', context={'foods_intolerances': foods_intolerances})