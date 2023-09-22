# foodplan
[Учебный проект dvmn](https://dvmn.org/modules/)

Cайт с рецептами по подписке. В том числе по планированию рациона, затратам на еду, диетам и так далее

<img width="1153" alt="image" src="https://github.com/Prikur76/foodplan/assets/55636018/2c32f7e4-0780-41b3-94dc-cb1a6d06b8a6">


## Требования к окружению 
Уставновить [Python 3.10](https://www.python.org/downloads/)    
Скачайте репозиторий.
Установите, создайте и активируйте виртуальное окружение:
```
pip3 install virtualenv
python3 -m venv env
source env/bin/activate
```
Установите библиотеки командой: 
```
pip3 install -r requirements.txt
```

## Переменные окружения     
Создайте файл ".env" (в него надо прописать ваши настройки)  

`ACCOUNT_ID` - айди магазина          
`U_KEY` - ключ эквайринга           
`DEBUG` - режим отладки              
`SECRET_KEY` - секретный ключ    
`ALLOWED_HOSTS` - Список хостов/доменов, для которых может работать текущий сайт.    
     
Пример .env файла    
```
ACCOUNT_ID=237136
U_KEY='test_8veJnrLUb09Z9rU5B_kFryjyJwDfiThi8cI926tTxN0'
SECRET_KEY=123qwe123
DEBUG=false
ALLOWED_HOSTS=webargs,konch,ped
```

- Оплата сделана через севрис [Юкасса](https://yookassa.ru). Необходимо зарегестрироваться и получить ID  магазина и API  ключ

## Запуск кода  


Вы можете создать ключ выполнив команду
```
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Создайте файл базы данных SQLite и отмигрируйте её следующей командой:
```
python .\manage.py migrate  
```

Создайте супер пользователя
```
python manage.py createsuperuser
```

Соберите статику
```
python manage.py collectstatic
```

Запустите сервер:
```
python manage.py runserver
```

Откройте сайт в браузере по адресу http://127.0.0.1:8000/.

## Отказ от ответственности:
Авторы программы не несут никакой ответственности за то, как вы используете этот код или как вы используете сгенерированные с его помощью данные. Эта программа была написана для обучения и других целей не несет. Не используйте данные, сгенерированные с помощью этого кода в незаконных целях.
