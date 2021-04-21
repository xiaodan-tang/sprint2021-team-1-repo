# DineLine
**Main**

[![gcivil-nyu-org](https://circleci.com/gh/gcivil-nyu-org/spring2021-cs-gy-9223-class/tree/main.svg?style=svg)](https://app.circleci.com/pipelines/github/gcivil-nyu-org/spring2021-cs-gy-9223-class?branch=main)
[![Coverage Status](https://coveralls.io/repos/github/gcivil-nyu-org/spring2021-cs-gy-9223-class/badge.svg?branch=main)](https://coveralls.io/github/gcivil-nyu-org/spring2021-cs-gy-9223-class?branch=main)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)


**Team-1**

[![gcivil-nyu-org](https://circleci.com/gh/gcivil-nyu-org/spring2021-cs-gy-9223-class/tree/team-1.svg?style=svg)](https://app.circleci.com/pipelines/github/gcivil-nyu-org/spring2021-cs-gy-9223-class?branch=team-1)
[![Coverage Status](https://coveralls.io/repos/github/gcivil-nyu-org/spring2021-cs-gy-9223-class/badge.svg?branch=team-1)](https://coveralls.io/github/gcivil-nyu-org/spring2021-cs-gy-9223-class?branch=team-1)

**Team-2**

[![gcivil-nyu-org](https://circleci.com/gh/gcivil-nyu-org/spring2021-cs-gy-9223-class/tree/team-2.svg?style=svg)](https://app.circleci.com/pipelines/github/gcivil-nyu-org/spring2021-cs-gy-9223-class?branch=team-2)
[![Coverage Status](https://coveralls.io/repos/github/gcivil-nyu-org/spring2021-cs-gy-9223-class/badge.svg?branch=team-2)](https://coveralls.io/github/gcivil-nyu-org/spring2021-cs-gy-9223-class?branch=team-2)



A dine-in app that leverages daily COVID-19 data to provide updated compliance status and hot spot notifications for reopened NYC restaurants.

https://dineline.herokuapp.com/


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


### 5) Initialize Data
For the first time deployment, to update the data model and initialize that database, use this command:
~~~shell
bash release-tasks.sh
~~~
All the commands that are run by this script can be viewed in release-tasks.sh



### 6) Create local superuser

~~~shell
python manage.py createsuperuser
~~~



### 7） Collect static files

~~~shell
python manage.py collectstatic
~~~



### 8) Run server

~~~shell
python manage.py runserver
~~~

Congratulations! Initial local deployment is all set and now you can visit the default url of this project to see the webpage.
