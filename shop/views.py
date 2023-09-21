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


def auth(request):

    return render(request, 'lk/auth.html', context={})


def registration(request):

    return render(request, 'lk/registration.html', context={})


def cabinet(request):

    return render(request, 'lk/lk.html', context={})


def order(request):
    foods_intolerances = FoodIntolerance.objects.all()
    context = {
        'foods_intolerances': foods_intolerances,
        'month_price': 300,
    }
    if request.GET:
        order = {
            'month_duration': request.GET['month_duration'],
            'breakfast': request.GET['breakfast'],
            'lunch': request.GET['Lunch'],
            'dinner': request.GET['Dinner'],
            'dessert': request.GET['dessert'],
            'people_number': request.GET['people_number'],
        }

    return render(request, 'shop/order.html', context=context)