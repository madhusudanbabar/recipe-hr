# Django Recipe API

A recipe sharing platform built using DRF

# Development
To start the development server follow these steps:
- Create a virtulenv `python -m venv .venv`
- source the virtualenv `source .venv/bin/activate`
- install the packages `pip install -r requirements.txt`
- start the development server `python manage.py runserver`
- ensure that you have running postgres instance
- if you get migration related warnings, run `python manage.py migrate`

# Deployment
To deploy the app on render, follow these steps:
- Sign up/log in to render
- create a new web service
- add build command `pip install -r requirements.txt && python manage.py migrate`
- add start command `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`