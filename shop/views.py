from django.shortcuts import render, redirect
from foods.models import Dish, FoodIntolerance, Order
from yookassa import Configuration, Payment
from environs import Env
import uuid
import socket
from food_plan.settings import ACCOUNT_ID, U_KEY


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
        order_data = {
            'month_duration': int(request.GET['month_duration']),
            'breakfast': request.GET['breakfast'],
            'lunch': request.GET['lunch'],
            'dinner': request.GET['dinner'],
            'dessert': request.GET['dessert'],
            'people_number': int(request.GET['people_number']),
            'intolerances': [],
        }
        for foods_intolerance in foods_intolerances:
            foods_intolerance = str(foods_intolerance)
            if foods_intolerance in request.GET:
                intolerance_id = request.GET[foods_intolerance]
                order_data['intolerances'].append(foods_intolerances.get(id=intolerance_id))

        order = Order.objects.create(
            breakfast=order_data['breakfast'],
            dinner=order_data['dinner'],
            lunch=order_data['lunch'],
            dessert=order_data['dessert'],
            people_count=order_data['people_number'],
            month_count=order_data['month_duration'],
            total_sum=round(MONTH_PRICE * order_data['month_duration'], 2),
        )
        order.intolerance.set(order_data['intolerances'])

        description = f"""
                    Подписка на {order.month_count} месяц(а)
                    Аллергены: {[intolerance.name for intolerance in order_data['intolerances']]}
                """
        http_host = request.META['HTTP_HOST']

        confirmation_url = create_payment(ACCOUNT_ID, U_KEY, description, f'http://{http_host}', order)
        return redirect(confirmation_url)
    return render(request, 'shop/order.html', context=context)


def create_payment(account_id, u_key, description, return_url, order):
    Configuration.account_id = account_id
    Configuration.secret_key = u_key
    idempotence_key = str(uuid.uuid4())

    payment = Payment.create({
        "amount": {
            "value": f"{order.total_sum}",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": return_url,
        },
        "capture": True,
        "description": description,
        "metadata": {
            "order": order.id
        },
    }, idempotence_key)

    confirmation_url = payment.confirmation.confirmation_url
    return confirmation_url

