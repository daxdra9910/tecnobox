# TecnoBox
A tech online shop built with Django.

**Used technologies**: *Python, JavaScript, HTML, CSS*.

---

## Installation

### 1. Clone git repository
After cloned, we are located in the repository folder.

~~~
$ git clone https://github.com/anferubu/tecnobox.git
$ cd tecnobox
~~~

### 2. Creation of a virtual environment
After created, we activate the environment.

~~~
$ python -m venv .venv
$ source .venv/Scripts/activate
~~~

### 3. Installation of dependencies

~~~
(.venv)$ python -m pip install -r requirements.txt 
~~~

### 4. Creation of a database
Open the PostgreSQL console and create a new database.

~~~
postgres> CREATE DATABASE YourDatabaseName;
~~~

### 5. Setting environment variables
Create a copy of `config/.env.example` and rename it as `.env` in the same directory. Then, fill in the values of the environment variables listed there.

~~~
SECRET_KEY=YoUrSeCrEtKeY
DEBUG=True

ALLOWED_HOSTS=host1,host2
CSRF_TRUSTED_ORIGINS=origin1,origin2

DB_ENGINE=django.db.backends.postgresql
DB_NAME=YourDatabaseName
DB_USER=postgres
DB_PASSWORD=YourDatabasePassword
DB_HOST=localhost
DB_PORT=

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_USE_TLS=True
EMAIL_PORT=587
EMAIL_HOST=YourEmailHost
EMAIL_HOST_USER=YourEmailAddress
EMAIL_HOST_PASSWORD=YourEmailPassword
~~~

### 6. Perform the necessary migrations
The migrations will create the necessary tables in the previously configured database.

~~~
(.env)$ python manage.py makemigrations
(.env)$ python manage.py migrate
~~~

### 7. Create a super user
Superuser will allow you to access the admin interface at the URL */dashboard/*.

~~~
(.env)$ python manage.py createsuperuser
~~~

### 8. Run the development server
Once the server is running, you will be able to see the project at the URL *127.0.0.1:8000/*.

~~~
(.env)$ python manage.py runserver
~~~
