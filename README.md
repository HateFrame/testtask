# Сайт знакомств
***

### Настройка Перед запуском

Добавьте виртуальное окружение
```
python3 -m venv venv

linux/Mac:
source venv/bin/activate

Windows:
source venv/Scripts/activate
```

Установите зависимости из requirements.txt

```
pip install -r requirements.txt
```

Выполните миграции
```
python manage.py migrate
```

Соберите статику
```
python manage.py collectstatic
```
Добавьте свои данные для доступа в .env по примеру из .env.example

```
SECRET_KEY=django secter key
EMAIL_HOST_USER=Почта с которой будут отсылаться письма пользователям
EMAIL_HOST_PASSWORD=Пароль от почты с которой будут отсылаться письма
DB_NAME=Имя базы данных
DB_USER=Имя пользователя бд
DB_USER_PASSWORD=Пароль пользователя бд
DB_HOST=Адрес сервера с бд
DB_PORT=Порт сервера
```
***
### Настройка базы данных
Установить расширение для бд [PostGIS](https://postgis.net/).

Установить библеотеку для чтения и записи растровых и векторных гео-пространственных форматов данных [GDAL](https://gdal.org/)

Для Windows удобнее всего будет воспользоваться [OSGeo4W](https://trac.osgeo.org/osgeo4w/)
***
### Запуск проекта

Создайте суперпользователя с правами администратора
```
python manage.py createsuperuser
```

Запустите проект
```
python manage.py runserver
```
***
## API

#### Доступно всем пользователям:
Создание нового пользователя:
```
/api/clients/create/ 

{
  "username": "testuser",
  "email": "testmail@test.com",
  "first_name": "test_name",
  "last_name": "test_last_name",
  "gender": "Male",
  "password": "password",
  "location":{
        "latitude": 64.000000,
        "longitude": -94.000000
    }
}
```
Получение refresh токена и access токена:
```
/api/token/
```
Проверка токена:
```
/api/token/verify/
```
Обновление токена:
```
/api/token/refresh/
```
В проекте добавлен Swagger:
```
/swagger
```
### Доступно только авторизированным пользователям
Для авторизации необходимо добавить в Header
```
Authorization: Bearer <token>
```

Добавление пользователя в список понравившихся:
```
api/clients/<int:id>/match
```
Вывод списка пользователей:
```
clients/list

Нечеткая фильтрация по полям first_name и last_name

api/list/?first_name=Имя пользователя   -   Фильтрация по имени
api/list/?last_name=Фамилия пользователя    -   Фильтрация по фамилии
api/list/?gender=Male   -   Фильтрация по половой принадлежности (Male или Female)
api/list/?distance=Расстояние в метрах  -   Фильрация по расстроянию

Также фильтры можно комбинировать:
api/list/?first_name=Имя&last_name=Фамилия&gender=Male&distance=1024
Выведет всех людей у которых имя содержит "Имя", фамилия содержит "Фамилия",
имеют мужской пол и находятся не дальше чем 1024 метра от точки,
указанной при регистрации пользователя.
```
***
## Ссылка на задеплоенный проект на хостинге heroku

https://testtaskdrf.herokuapp.com/
