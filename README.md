# DineLine
**Main**

[![Build Status](https://travis-ci.com/xiaodan-tang/sprint2021-team-1-repo.svg?branch=main)](https://travis-ci.com/xiaodan-tang/sprint2021-team-1-repo)
[![Coverage Status](https://coveralls.io/repos/github/xiaodan-tang/sprint2021-team-1-repo/badge.svg?branch=main)](https://coveralls.io/github/xiaodan-tang/sprint2021-team-1-repo?branch=main)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)


A dine-in app that leverages daily COVID-19 data to provide updated compliance status and hot spot notifications for reopened NYC restaurants.

https://dine-safe-ly.herokuapp.com/


## 1. How to set up local environment

### 1) Clone the repo into local environment
Use git clone with the repo's link


### 2) Create an virtual environment of Python to work on this project

replace ***name_of_venv*** with the name you wanted for the virtual environment

~~~shell
python3 -m venv name_of_venv
~~~



### 3) Activate the venv and install the required libraries for this project

~~~shell
# Activate the virtual environment
source name_of_venv/bin/activate

# Install required libraries
pip install -r requirements.txt
~~~



### 4) Create a .env file to store all the related keys

For security issues, all the keys for this project are separately stored in environmental variables and loaded during running time. Thus, in order to deploy and build locally, creating a .env file and set up all the keys is mandatory.

All the related key_names can be found in  ***dinesafelysite/settings.py*** with a format of

~~~python
XXX_KEY = os.environ.get("XXX_KEY")
~~~

To set up corresponding key in .env, simply add the key in this format:

~~~:
XXX_KEY="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
~~~



### 5) Migrations

For the first time deployment, if there's an update on any model, a makemigrations is needed before migration operation. Make migrations using this command:

~~~shell
python manage.py makemigrations
~~~

If there's nothing changed on model, execute a migration to generate the underlying database.

~~~:
python manage.py migrate
~~~



### 6) Load initial data to database

~~~shell
python manage.py loaddata data.json
~~~

This process might take some time since the initial dataset is a little bit large.



### 7) Create local superuser

~~~shell
python manage.py createsuperuser
~~~



### 8） Collect static files

~~~shell
python manage.py collectstatic
~~~



### 9) Run server

~~~shell
python manage.py runserver
~~~

Congratulations! Initial local deployment is all set and now you can visit the default url of this project to see the webpage.
