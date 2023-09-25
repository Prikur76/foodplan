import uuid
from urllib.parse import urlencode

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from yookassa import Configuration, Payment

from customers.models import Customer
from food_plan.settings import ACCOUNT_ID, U_KEY
from foods.models import Dish, FoodIntolerance, Order
from .forms import UserRegistrationForm, AuthForm


def index(request):
    dishes = Dish.objects.filter(is_active=True)[:3]
    if 'order_id' in request.GET:
        order = Order.objects.get(id=request.GET['order_id'])
        payment_id = order.yookassa_id
        Configuration.account_id = ACCOUNT_ID
        Configuration.secret_key = U_KEY
        payment = Payment.find_one(payment_id)
        if payment.paid:
            order.paid = True
            order.save()
    context = {
        'dishes': dishes
    }
    return render(request, 'shop/index.html', context=context)

def contacts(request):
    return render(request, 'shop/contact.html', context={})


def auth(request):
    if request.method == 'POST':
        form = AuthForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['email'],
                                password=cd['password'])
            if user.is_active:
                login(request, user,
                      backend='shop.authentication.EmailAuthBackend')
                return redirect('/account/')
    else:
        form = AuthForm()
        return render(request,
                      template_name='account/auth.html',
                      context={'form': form})


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            login(request, new_user,
                  backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/auth/')
    else:
        form = UserRegistrationForm()
    return render(request,
                  template_name='account/registration.html',
                  context={'form': form})


# def registration(request):
#     context = {
#         'user': '',
#         'created': False,
#     }
#     if 'name' and 'email' and 'password' and 'password_confirm' in request.GET:
#         user, created = User.objects.get_or_create(
#             username=request.GET['name'],
#             email=request.GET['email'],
#             password=request.GET['password'],
#         )
#         context = {'user': user, 'created': created}
#
#     return render(request, 'account/registration.html', context=context)


@login_required(login_url='/auth/')
def account(request):
    user = Customer.objects.get(username=request.user)
    persons_count = '0'
    intolerances = '0'
    try:
        order = Order.objects.filter(customer=request.user, paid=True).first()
        if order:
            persons_count = str(order.people_count)
            intolerances = str(order.intolerance.count())
    except Order.DoesNotExist:
        order = None

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user.username = form.cleaned_data['username']
            if form.cleaned_data['username'] != request.user.username:
                user.save(update_fields=('username'))
            user.password = form.cleaned_data['password1']
            if form.cleaned_data['password1'] != request.user.password:
                user.save(update_fields=('password'))
            login(request, user,
                  backend='shop.authentication.EmailAuthBackend')
            return redirect('/auth/')
    else:
        form = UserRegistrationForm()

        context = {
            'user': user,
            'orders': order,
            'persons_count': persons_count,
            'intolerances': intolerances,
            'form': form
        }
        return render(request,
                      template_name='account/lk.html',
                      context=context)


def logout(request):
    return render(request, 'account/logout.html')


@login_required()
def order_view(request):
    user = Customer.objects.get(username=request.user)
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
            customer=user,
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
        return_url = f'http://{request.META["HTTP_HOST"]}/?' + urlencode({'order_id': order.id})

        payment = create_payment(ACCOUNT_ID, U_KEY, description, return_url, order)
        confirmation_url = payment.confirmation.confirmation_url

        order.yookassa_id = payment.id
        order.save()

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

    return payment

