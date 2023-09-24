from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from tinymce.models import HTMLField
from django.conf import settings

from customers.models import Customer


# Create your models here.
class FoodIntolerance(models.Model):
    """Список аллергенов"""
    name = models.CharField(max_length=255, verbose_name='название')

    class Meta:
        verbose_name = 'аллерген'
        verbose_name_plural = 'список аллергенов'

    def __str__(self):
        return self.name


class Dish(models.Model):
    """Описание блюда"""
    name = models.CharField(
        max_length=255, verbose_name='название')
    slogan = models.CharField(
        max_length=255, verbose_name='слоган', null=True)
    slug = models.SlugField(
        max_length=100, unique=True,
        verbose_name='slug')
    dish_types = (
        ('salad', 'салат'),
        ('soup', 'суп'),
        ('second_dish', 'второе блюдо'),
        ('bakery', 'выпечка'),
        ('dessert', 'десерт'),
        ('drink', 'напиток'),
        ('other', 'другое'),
    )
    dish_type = models.CharField(
        max_length=15, choices=dish_types,
        verbose_name='тип блюда')

    mealtime_types = (
        ('breakfast', 'завтрак'),
        ('lunch', 'обед'),
        ('dinner', 'ужин'),
    )
    mealtime = models.CharField(
        max_length=15, choices=mealtime_types,
        verbose_name='время приема пищи')
    proteins = models.PositiveIntegerField(verbose_name='белки, на 100 г', default=0)
    fats = models.PositiveIntegerField(verbose_name='жиры, на 100 г', default=0)
    carbohydrates = models.PositiveIntegerField(verbose_name='углеводы, на 100 г', default=0)
    calories = models.PositiveIntegerField(verbose_name='калории, ккал', default=0)
    cooking_time = models.PositiveIntegerField(verbose_name='время приготовления, мин')
    dish_image = models.ImageField(
        verbose_name='изображение',
        blank=True)
    is_active = models.BooleanField(
        default=True, verbose_name='активно')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='дата создания')
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='дата обновления')

    class Meta:
        verbose_name = 'блюдо'
        verbose_name_plural = 'блюда'

    def __str__(self):
        return self.name


class CookingProduct(models.Model):
    """Характеристика продукта в составе блюда"""
    name = models.CharField(max_length=255, verbose_name='наименование')
    allergens = models.ManyToManyField(
        FoodIntolerance, related_name='foods',
        blank=True, verbose_name='Аллергены')
    needed_for_dishes = models.ManyToManyField(
        Dish, through='foods.Ingredient',
        related_name='foods', verbose_name='блюдо')
    image = models.ImageField(
        upload_to='foods/',
        verbose_name='изображение',
        blank=True)

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    dish = models.ForeignKey(
        Dish, on_delete=models.CASCADE,
        related_name='ingredients', verbose_name='блюдо')
    cooking_product = models.ForeignKey(
        CookingProduct, on_delete=models.CASCADE,
        related_name='ingredients', verbose_name='продукт')
    quantity = models.FloatField(default=0.0, verbose_name='количество')
    units = (
        ('g', 'г'),
        ('kg', 'кг'),
        ('l', 'л'),
        ('ml', 'мл'),
        ('pcs', 'шт'),
        ('tablespoon', 'ст.л.'),
        ('teaspoon', 'ч.л.'),
        ('pack', 'упаковка'),
        ('bottle', 'бутылка'),
        ('portion', 'порция'),
        ('box', 'коробка'),
        ('cup', 'чашка'),
        ('to_taste', 'по вкусу'),
        ('other', 'другое'),
    )
    measure_unit = models.CharField(
        max_length=15, choices=units, verbose_name='ед. изм.')

    class Meta:
        verbose_name = 'состав'
        verbose_name_plural = 'состав'

    def __str__(self):
        return f'{self.dish}: {self.cooking_product} ({self.quantity} {self.measure_unit})'


class Stage(models.Model):
    step_name = models.CharField(
        max_length=255, verbose_name='шаг')
    description = models.TextField(verbose_name='описание шага')
    image = models.ImageField(
        upload_to='stages/', verbose_name='изображение',
        blank=True)

    class Meta:
        verbose_name = 'этап'
        verbose_name_plural = 'этапы'

    def __str__(self):
        return self.step_name


class Recipe(models.Model):
    """Рецепт блюда"""
    name = models.CharField(
        max_length=250, verbose_name='наименование')
    slug = models.SlugField(
        max_length=100, unique=True, verbose_name='slug')
    dish = models.ForeignKey(
        Dish, on_delete=models.CASCADE,
        related_name='recipes', verbose_name='блюдо')
    cooking_steps = models.ManyToManyField(
        Stage, related_name='recipes', verbose_name='этапы приготовления')
    short_description = models.CharField(
        max_length=255, verbose_name='краткое описание', blank=True)
    description = HTMLField(
        verbose_name='описание',
        blank=True
    )
    is_active = models.BooleanField(
        default=True, verbose_name='активно')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='дата создания')
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='дата обновления')

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self):
        return f'{self.name}: {self.dish}'


class MenuType(models.Model):
    name = models.CharField(
        max_length=100, verbose_name='тип меню')
    valid_from = models.DateTimeField(verbose_name='действительно с')
    valid_to = models.DateTimeField(verbose_name='действительно до')
    dishes = models.ManyToManyField(
        Dish, related_name='menu_types',
        verbose_name='блюда')
    is_active = models.BooleanField(
        default=True, verbose_name='активно?')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='дата создания')
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='дата обновления')

    class Meta:
        verbose_name = 'тип меню'
        verbose_name_plural = 'типы меню'

    def __str__(self):
        return self.name


class Order(models.Model):
    breakfast = models.BooleanField(verbose_name='Завтрак', default=False)
    dinner = models.BooleanField(verbose_name='Ужин', default=False)
    lunch = models.BooleanField(verbose_name='Обед', default=False)
    dessert = models.BooleanField(verbose_name='Десерты', default=False)
    people_count = models.IntegerField(verbose_name='Кол-во людей', default=1)
    month_count = models.IntegerField(verbose_name='Кол-во месяцев', default=1)
    intolerance = models.ManyToManyField(FoodIntolerance, related_name='orders')
    paid = models.BooleanField(verbose_name='оплачено', default=False)
    start_date = models.DateTimeField('Дата заказа', db_index=True, default=now)
    yookassa_id = models.CharField(verbose_name='yookassa id',  max_length=64)
    total_sum = models.DecimalField(
        verbose_name='сумма заказа',
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    def __str__(self):
        if self.paid:
            return f'{self.id} Оплачен'
        return f'{self.id} Не оплачен'


class CustomerOrder(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE,
        related_name='customers',
        verbose_name='заказ')
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='клиент')
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата создания')

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы клиентов'

    def __str__(self):
        return f'{self.customer} - {self.order}'
