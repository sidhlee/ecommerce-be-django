# E-Commerce Django Backend

A code-along repo for the backend part of the course: [Django with React | An Ecommerce Website](https://www.udemy.com/course/django-with-react-an-ecommerce-website/).

## Setting up Django project

Open up Windows Powershell and run the following:

1. Install python
2. Setup virtual env by `python -m venv myenv`
3. Activate venv by `myenv/Scripts/activate` on Windows, `source myenv/bin/activate` on Linux
4. Install Django `pip install django`
5. Create Django Project `django-admin startproject ecomm_backend`
6. Create .gitignore by visiting gitignore.io and search django + windows or macos.
7. Create .env and copy&paste SECRET_KEY from `settings.py`
8. Use decouple library to replace secret from settings.py with the env variable
9. Add `.gitignore` from gitignore.io. Search by django and windows10
10. Pin the dependency versions `python -m pip freeze > requirements.txt`
11. Init git `git init`
12. Commit and Push
13. Run server by going inside the project folder you created in step 5 and run `python manage.py runserver`
14. Add more apps by `python manage.py startapp base` and registering it to `INSTALLED_app` list inside `settings.py`

## Django-Cors-Headers

To allow in-browser requests to your Django-app from other origins, you can install [django-cors-headers](https://github.com/adamchainz/django-cors-headers).

## Troubleshoot

### Rest_Framework: Error: OperationalError at /api/ no such table: django_session

You need to run migrations to make django_session available. Refer to this [article](https://thequickblog.com/django-rest-framework-operationalerror-no-such-table-django-session/)

```bash
python manage.py makemigrations
python manage.py migrate
```

### Accidentally deleted the migrations folder

- [S.O](https://stackoverflow.com/a/60522931)
- [Working Solution](https://simpleisbetterthancomplex.com/tutorial/2016/07/26/how-to-reset-migrations.html)

## Reference

- [Your first steps with Django: Set up a Django project](https://realpython.com/django-setup/)
