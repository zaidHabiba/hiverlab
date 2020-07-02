# Django Project

The clean, fast and right way to start a new Django `2.2.5` powered website.

## Getting Started

Setup project environment with [virtualenv](https://virtualenv.pypa.io) and [pip](https://pip.pypa.io).

```bash
$ virtualenv project-env
$ source project-env/bin/activate
```
Or
```bash
$ conda create --name env
$ source env/bin/activate
```
Then Run:
```bash
$ pip install -r requirements.txt

$ python manage.py migrate
$ python manage.py runserver 0.0.0.0:8000
```
To create admin user
```bash
$ py manage.py createsuperuser
```
