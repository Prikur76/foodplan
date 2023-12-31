# Generated by Django 4.2.5 on 2023-09-19 17:44

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CookingProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='наименование')),
                ('image', models.ImageField(blank=True, upload_to='foods/', verbose_name='изображение')),
            ],
            options={
                'verbose_name': 'продукт',
                'verbose_name_plural': 'продукты',
            },
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='название')),
                ('slug', models.SlugField(blank=True, max_length=100, unique=True, verbose_name='slug')),
                ('dish_type', models.CharField(choices=[('salad', 'салат'), ('soup', 'суп'), ('second_dish', 'второе блюдо'), ('bakery', 'выпечка'), ('dessert', 'десерт'), ('drink', 'напиток'), ('other', 'другое')], max_length=15, verbose_name='тип блюда')),
                ('mealtime', models.CharField(choices=[('breakfast', 'завтрак'), ('lunch', 'обед'), ('dinner', 'ужин')], max_length=15, verbose_name='время приема пищи')),
                ('proteins', models.PositiveIntegerField(default=0, verbose_name='белки, на 100 г')),
                ('fats', models.PositiveIntegerField(default=0, verbose_name='жиры, на 100 г')),
                ('carbohydrates', models.PositiveIntegerField(default=0, verbose_name='углеводы, на 100 г')),
                ('calories', models.PositiveIntegerField(default=0, verbose_name='калории, ккал')),
                ('cooking_time', models.PositiveIntegerField(verbose_name='время приготовления, мин')),
                ('dish_image', models.ImageField(blank=True, upload_to='dishes/', verbose_name='изображение')),
                ('is_active', models.BooleanField(default=True, verbose_name='активно')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='дата обновления')),
            ],
            options={
                'verbose_name': 'блюдо',
                'verbose_name_plural': 'блюда',
            },
        ),
        migrations.CreateModel(
            name='FoodIntolerance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='название')),
            ],
            options={
                'verbose_name': 'аллерген',
                'verbose_name_plural': 'список аллергенов',
            },
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step_name', models.CharField(max_length=255, verbose_name='шаг')),
                ('description', models.TextField(verbose_name='описание шага')),
                ('image', models.ImageField(blank=True, upload_to='stages/', verbose_name='изображение')),
            ],
            options={
                'verbose_name': 'этап',
                'verbose_name_plural': 'этапы',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='наименование')),
                ('slug', models.SlugField(blank=True, max_length=100, unique=True, verbose_name='slug')),
                ('short_description', models.CharField(blank=True, max_length=255, verbose_name='краткое описание')),
                ('description', tinymce.models.HTMLField(blank=True, verbose_name='описание')),
                ('is_active', models.BooleanField(default=True, verbose_name='активно')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='дата обновления')),
                ('cooking_steps', models.ManyToManyField(related_name='recipes', to='foods.stage', verbose_name='этапы приготовления')),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to='foods.dish', verbose_name='блюдо')),
            ],
            options={
                'verbose_name': 'рецепт',
                'verbose_name_plural': 'рецепты',
            },
        ),
        migrations.CreateModel(
            name='MenuType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='тип меню')),
                ('valid_from', models.DateTimeField(verbose_name='действительно с')),
                ('valid_to', models.DateTimeField(verbose_name='действительно до')),
                ('is_active', models.BooleanField(default=True, verbose_name='активно?')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='дата обновления')),
                ('dishes', models.ManyToManyField(related_name='menu_types', to='foods.dish', verbose_name='блюда')),
            ],
            options={
                'verbose_name': 'тип меню',
                'verbose_name_plural': 'типы меню',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(default=0.0, verbose_name='количество')),
                ('measure_unit', models.CharField(choices=[('g', 'г'), ('kg', 'кг'), ('l', 'л'), ('ml', 'мл'), ('pcs', 'шт'), ('tablespoon', 'ст.л.'), ('teaspoon', 'ч.л.'), ('pack', 'упаковка'), ('bottle', 'бутылка'), ('portion', 'порция'), ('box', 'коробка'), ('cup', 'чашка'), ('to_taste', 'по вкусу'), ('other', 'другое')], max_length=15, verbose_name='ед. изм.')),
                ('cooking_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='foods.cookingproduct', verbose_name='продукт')),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='foods.dish', verbose_name='блюдо')),
            ],
            options={
                'verbose_name': 'ингредиент',
                'verbose_name_plural': 'ингредиенты',
            },
        ),
        migrations.AddField(
            model_name='cookingproduct',
            name='allergens',
            field=models.ManyToManyField(blank=True, related_name='foods', to='foods.foodintolerance', verbose_name='Аллергены'),
        ),
        migrations.AddField(
            model_name='cookingproduct',
            name='needed_for_dishes',
            field=models.ManyToManyField(related_name='foods', through='foods.Ingredient', to='foods.dish', verbose_name='блюдо'),
        ),
    ]
