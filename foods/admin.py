from django.contrib import admin
from .models import (FoodIntolerance, Dish,
                     CookingProduct, Ingredient,
                     Stage, Recipe, MenuType, Order,
                   )
from customers.models import Customer


# Register your models here.
@admin.register(FoodIntolerance)
class FoodIntoleranceAdmin(admin.ModelAdmin):
    pass


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ['name', 'slogan', 'slug', 'dish_image', 'dish_type',
                    'mealtime', 'cooking_time',  'calories',
                    'proteins', 'fats', 'carbohydrates',
                    ]
    list_per_page = 20
    filtered_fields = ['dish_type', 'mealtime', 'is_active']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = [
        (None, {'fields': [
            ('name', 'slogan', 'slug'),
            ('dish_type', 'mealtime'),
            'cooking_time', 'dish_image'
        ]}),
        ('Пищевая ценность', {'fields': [
            ('calories', 'proteins'),
            ('fats', 'carbohydrates')
        ]}),
        ('Дополнительно', {'fields': [
            'is_active', ('created_at', 'updated_at')]}),
    ]


@admin.register(CookingProduct)
class CookingProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'image']
    raw_id_fields = ['needed_for_dishes', 'allergens']
    list_per_page = 20


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['dish', 'cooking_product', 'quantity', 'measure_unit']
    list_per_page = 20


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ['step_name', 'description', 'image']
    list_per_page = 20


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    # inlines = [StageTabularInline]
    list_display = ['name', 'slug', 'dish', 'short_description', 'description']
    list_per_page = 20
    raw_id_fields = ['cooking_steps']


@admin.register(MenuType)
class MenuTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'valid_from', 'valid_to']
    raw_id_fields = ['dishes']
    list_filter = ['is_active', 'valid_from', 'valid_to']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ['start_date', 'yookassa_id']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass

