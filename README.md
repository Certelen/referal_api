# Реферальная API
## Описание
API позволяет пользователям регистрироваться, необязательно указывая реферальный код другого пользователя.

## Технологии
- Python 3.11
- Django 5.0.2
- Django REST Framework 3.14.0
- PostgreSQL 13.0
- Nginx 1.21.3
- Docker
- Docker-compose

# Установка
## Копирование репозитория
Клонируем репозиторий:
```
~ git clone git@github.com:Certelen/referal_api.git
```
Требуется изменить:
В файле ./infra/nginx/default.conf значения server_name и listen на нужный адрес и порт.
В файле ./infra/docker-compose.yml значение nginx/ports на нужный порт.

Выбрать один из двух вариантов запуска:

## 1. Развертывание на боевом сервере:
Переходим в директорию infra:
```
~ cd ./referal_api/infra/
```
1. Перейдите на боевой сервер:
```
ssh username@server_address
```
2. Обновите индекс пакетов APT:
```
sudo apt update
```
и обновите установленные в системе пакеты и установите обновления безопасности:
```
sudo apt upgrade -y
```
Создайте папку `nginx`:
```
mkdir nginx
``` 
Скопируйте файлы docker-compose.yaml, nginx/default.conf из вашего проекта на сервер в home/<ваш_username>/docker-compose.yaml, home/<ваш_username>/nginx/default.conf соответственно:
```
scp docker-compose.yaml <username>@<host>/home/<username>/docker-compose.yaml
scp default.conf <username>@<host>/home/<username>/nginx/default.conf
```
Установите Docker и Docker-compose:
```
sudo apt install docker.io
```
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
```
sudo chmod +x /usr/local/bin/docker-compose
```
Проверьте правильность установки Docker-compose:
```
sudo  docker-compose --version
```
На боевом сервере создайте файл .env:
```
touch .env
```
и заполните переменные окружения
```
nano .env
- POSTGRES_DB = <Имя базы данных>
- POSTGRES_USER = <Имя пользователя базы данных>
- POSTGRES_PASSWORD = <Пароль пользователя базы данных>
- POSTGRES_HOST = <Адрес базы данных>
- POSTGRES_PORT = <Порт базы данных>

- EMAIL_HOST = <Адрес почтового сервиса>
- EMAIL_PORT = <Порт используемый почтовым сервисом>
- EMAIL_HOST_USER = <Ник аккаунта почтового сервиса>
- EMAIL_HOST_PASSWORD = <Пароль аккаунта почтового сервиса>
- EMAIL_USE_SSL = <True/False - выбрать использует ли данный протокол почтовый сервис>
- EMAIL_USE_TLS = <True/False - выбрать использует ли данный протокол почтовый сервис>

- WEB_HOST = <Адрес сервера>
- WEB_PORT = <Порт сервера>
```
Разворачиваем контейнеры в фоновом режиме из папки infra:
```
sudo docker compose up -d
```
При первом запуске выполняем миграции:
```
sudo docker compose exec backend python manage.py migrate
```
И собираем статику:
```
sudo docker compose exec backend python manage.py collectstatic --no-input
```
Создаем суперпользователя:
```
sudo docker compose exec backend python manage.py createsuperuser
```

## 2. Развертывание на текущем устройстве:
Устанавливаем и активируем виртуальное окружение из папки с проектом
```
~ py -3.11 -m venv venv
~ . venv/Scripts/activate
```
Устанавливаем требуемые зависимости:
```
~ pip install -r requirements.txt
```
Создайте .env файл и заполните переменные окружения в нем
```
- POSTGRES_DB = <Имя базы данных>
- POSTGRES_USER = <Имя пользователя базы данных>
- POSTGRES_PASSWORD = <Пароль пользователя базы данных>
- POSTGRES_HOST = <Адрес базы данных>
- POSTGRES_PORT = <Порт базы данных>

- EMAIL_HOST = <Адрес почтового сервиса>
- EMAIL_PORT = <Порт используемый почтовым сервисом>
- EMAIL_HOST_USER = <Ник аккаунта почтового сервиса>
- EMAIL_HOST_PASSWORD = <Пароль аккаунта почтового сервиса>
- EMAIL_USE_SSL = <True/False - выбрать использует ли данный протокол почтовый сервис>
- EMAIL_USE_TLS = <True/False - выбрать использует ли данный протокол почтовый сервис>

- WEB_HOST = <Адрес сервера>
- WEB_PORT = <Порт сервера>
```
Перейдите в папку
```
~ cd referal_system
```
```
Перед первым запуском выполняем миграции:
```
python manage.py migrate
```
Создаем суперпользователя:
```
python manage.py createsuperuser
```
# Запуск
Запуск сервиса производится командой:
```
~ uvicorn referal_system.asgi:application
```
# Адресные пути
- [Документация к API базе данных](http://127.0.0.1/redoc)
- [Админ-панель базы данных](http://127.0.0.1/admin)
# Авторы
Дмитрий Коломейцев
