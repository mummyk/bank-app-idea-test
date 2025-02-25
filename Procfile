web: gunicorn --config gunicorn.conf.py core.wsgi

# Uncomment below if you want to work locally on windows and comment the above

# web: python manage.py runserver %PORT%

# Uncomment this `release` process if you are using a database, so that Django's model

# migrations are run as part of app deployment, using Heroku's Release Phase features

# <https://docs.djangoproject.com/en/5.1/topics/migrations/>

# <https://devcenter.heroku.com/articles/release-phase>

release: ./manage.py migrate --no-input
