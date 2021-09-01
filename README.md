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

## Django Contrib packages

Django's contrib packages include many tools that solve common web-development problems.
Contrib includes packages like admin, auth, humanize, messages, postgres, and redirects.

- [Documentation](https://docs.djangoproject.com/en/3.2/ref/contrib/)

## Resetting database in Django

Unlike NoSQL database like MongoDB, things can get tangled up pretty quick working with relational database, especially when you make many revisions to your fields.
You can reset your database in Django with the following steps:

## Django Views

A view is a function or method that takes a request and returns a response. Django

- Django Views = Express Routers + Controllers

You can use class-based view to improve the code structure and reusability through mixin

- [Introduction to class-based views](https://docs.djangoproject.com/en/3.2/topics/class-based-views/intro/)

### Reset SQLite3 Database

1. Delete `db.sqlite3` file
2. Delete all migrations folder
3. Make migrations by `python manage.py makemigrations`
4. If the migrations folders are not created for some applications, run the above command with app names as args: `python manage.py makemigrations base`

### Reset the whole Database

```bash
python manage.py flush
```

### Reverse all migrations for the 'base' app

```bash
python manage.py migrate base zero
```

- [Source](https://www.delftstack.com/howto/django/django-reset-database/)

## `null` and `blank` option in the Django model field

- [Documentation](https://docs.djangoproject.com/en/3.2/ref/models/fields/#null)
- If you set `null=True`, Django will set the empty values as 'NULL'
- `blank=True` allows you to leave the field blank when you're adding rows through admin forms or custom forms. It is the same as NOT having `required` on the form field.
- Those two are typically used together.
  > Avoid using null on string-based fields such as CharField and TextField. If a string-based field has null=True, that means it has two possible values for “no data”: NULL, and the empty string. In most cases, it’s redundant to have two possible values for “no data;” the Django convention is to use the empty string, not NULL. One exception is when a CharField has both unique=True and blank=True set. In this situation, null=True is required to avoid unique constraint violations when saving multiple objects with blank values.

## Authentication with Simple JWT

From [Django REST framework documentation](https://www.django-rest-framework.org/api-guide/authentication/#json-web-token-authentication)

> Unlike the built-in TokenAuthentication scheme, JWT Authentication doesn't need to use a database to validate a token. A package for JWT authentication is djangorestframework-simplejwt which provides some features as well as a pluggable token blacklist app.

[Simple JWT documentation](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)

### Changing the encoded value inside JWT

You can customize the "claims" in JWT by creating a subclass for

## Troubleshoot

### Rest_Framework: Error: OperationalError at /api/ no such table: django_session

You need to run migrations to make django_session available. Refer to this [article](https://thequickblog.com/django-rest-framework-operationalerror-no-such-table-django-session/)

```bash
python manage.py makemigrations
python manage.py migrate
```

### Python formatting not working

You need to turn off the editor's default formatter which is set to prettier.
Here's the python related settings.

`settings.json`

```json
{
  "python.linting.pylintArgs": [
    "--load-plugins=pylint_django",
    "--disable=django-not-configured",
    "--disabled=missing-module-docstring"
  ],
  "python.formatting.provider": "autopep8",
  "[python]": {
    "editor.defaultFormatter": null,
    "editor.tabSize": 4,
    "editor.formatOnSave": true
  },
  "[django-html]": {
    "editor.quickSuggestions": {
      "other": true,
      "comments": true,
      "strings": true
    },
    "editor.defaultFormatter": "vscode.html-language-features"
  }
}
```

### Accidentally deleted the migrations folder

- [S.O](https://stackoverflow.com/a/60522931)
- [Working Solution](https://simpleisbetterthancomplex.com/tutorial/2016/07/26/how-to-reset-migrations.html)

## Reference

- [Your first steps with Django: Set up a Django project](https://realpython.com/django-setup/)
