from django.shortcuts import render
from foods.models import Dish, FoodIntolerance, Order

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

def order_view(request):
    MONTH_PRICE = 300
    foods_intolerances = FoodIntolerance.objects.all()
    context = {
        'foods_intolerances': foods_intolerances,
        'month_price': MONTH_PRICE,
    }
    if request.GET:
        print(request.GET)
        order_data = {
            'month_duration': int(request.GET['month_duration']),
            'breakfast': request.GET['breakfast'],
            'lunch': request.GET['lunch'],
            'dinner': request.GET['dinner'],
            'dessert': request.GET['dessert'],
            'people_number': request.GET['people_number'],
            'intolerances': [],
        }
        for foods_intolerance in foods_intolerances:
            foods_intolerance = str(foods_intolerance)
            if foods_intolerance in request.GET:
                intolerance_id = request.GET[foods_intolerance]
                order_data['intolerances'].append(foods_intolerances.get(id=intolerance_id))

        print(order_data)

        order = Order.objects.create(
            breakfast=order_data['breakfast'],
            dinner=order_data['dinner'],
            lunch=order_data['lunch'],
            dessert=order_data['dessert'],
            people_count=int(order_data['people_number']),
            month_count=int(order_data['month_duration']),
            total_sum=round(MONTH_PRICE *order_data['month_duration'], 2),
        )
        order.intolerance.set(order_data['intolerances'])
        #
        # print(order)

    return render(request, 'shop/order.html', context=context)