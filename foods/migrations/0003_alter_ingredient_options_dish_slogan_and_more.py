# Generated by Django 4.2.5 on 2023-09-20 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0002_alter_dish_slug_alter_recipe_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'verbose_name': 'состав', 'verbose_name_plural': 'состав'},
        ),
        migrations.AddField(
            model_name='dish',
            name='slogan',
            field=models.CharField(max_length=255, null=True, verbose_name='слоган'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='dish_image',
            field=models.ImageField(blank=True, upload_to='', verbose_name='изображение'),
        ),
    ]
