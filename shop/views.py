from django.shortcuts import render, redirect
from foods.models import Dish, FoodIntolerance, Order
from yookassa import Configuration, Payment
from environs import Env
import uuid


env = Env()
env.read_env()
ACCOUNT_ID = env('ACCOUNT_ID')
U_KEY = env('U_KEY')


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

        Configuration.account_id = ACCOUNT_ID
        Configuration.secret_key = U_KEY

        desciption = f"""
            Подписка на {order.month_count} месяц(а)
            Аллергены: {[intolerance.name for intolerance in order_data['intolerances']]}
        """

        payment = Payment.create({
            "amount": {
                "value": f"{order.total_sum}",
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": '/'
            },
            "capture": True,
            "description": desciption,
            "metadata": {"order": order.id},
        }, uuid.uuid4())
        confirmation_url = payment.confirmation.confirmation_url
        return redirect(confirmation_url)

    return render(request, 'shop/order.html', context=context)
