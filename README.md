# HexOcean_task
Test task for junior python backend position.

## Install instructions

follow these steps to manually install and load this projects locally

### 1. Clone this repository

```shell
git clone https://github.com/ifhyy/HexOcean_task.git
cd Hexocean_task
```
### 2. Create and activate virtual environment

```shell
pip install virtualenv
virtualenv venv
source venv/bin/activate  # For Windows use venv\Scripts\activate
```

### 3. Download dependencies

```shell
pip install -r requirements.txt
```

### 4. Download PostgreSQL and create empty database
https://www.postgresql.org/download/

### 5. Configure database settings in setting.py

```shell
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '{your_database_name}',
        'USER': 'your_database_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost'
    }
}
```

### 6. Apply database migrations

```shell
python manage.py makemigrations
python manage.py migrate
python manage.py createcachetable
```

### 7. Create superuser for admin panel

```shell
python manage.py createsuperuser
```

### 8. Run Django development server

```shell
python manage.py runserver
```
Project will be available on http://localhost:8000

## Creator
This project was created by Artem Stupak
