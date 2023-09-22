# foodplan


## Установка

```commandline
python -m pip install -r requirements.txt
```
Перед запуском создайте файл .env вида:
```commandline
ACCOUNT_ID='ID вашего магазина'
U_KEY='Ключ к юкассе'
```
- Оплата сделана через севрис [Юкасса](https://yookassa.ru). Необходимо зарегестрироваться и получить ID  магазина и API  ключ

## Запуск
Вы можете создать ключ выполнив команду
```python
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

```
Создайте файл базы данных SQLite и отмигрируйте её следующей командой:

```python
python .\manage.py migrate  
```
Создайте супер пользователя
```python
python manage.py createsuperuser
```
Соберите статику
```python
python manage.py collectstatic
```

Запустите сервер:
```
python manage.py runserver
```

Откройте сайт в браузере по адресу http://127.0.0.1:8000/.