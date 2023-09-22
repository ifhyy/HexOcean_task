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

## How to use
Since this application is not supposed to have UI, you're going to need some platform to access API.
e.g. Postman would be appropriate tool for this.
In order to pass request parameters, include them in the request body.

### Authentication
Log in to start.

Two parameters required.
**username**
**password**

```shell
POST.    http://localhost:8000/api-auth/login/
```

### Image Upload
Allows user to upload an image whether .png or .jpg

Required parameter
**image** : a file consisting .png or .jpg image that will be turned into thumbnail

Optional parameter
**expiring_time_seconds : integer value between 300 and 300000 that specifies expiring link lifetime.
Causes generating an expiring link to originally uploaded image.
Note: users with no permission to create exp. links may not include this parameter.

```shell
POST.    http://localhost:8000/api/v1/images_upload/
```

## Creator
This project was created by Artem Stupak
