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

## Django Views

A view is a function or method that takes a request and returns a response. Django

- Django Views = Express Routers + Controllers

You can use class-based view to improve the code structure and reusability through mixin

- [Introduction to class-based views](https://docs.djangoproject.com/en/3.2/topics/class-based-views/intro/)

## Resetting database in Django

Unlike NoSQL database like MongoDB, things can get tangled up pretty quick working with relational database, especially when you make many revisions to your fields.
You can reset your database in Django with the following steps:

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

## Authentication with email instead of username

You can create a custom `User` model to use email instead of the default "username" field.

1. Create "accounts" app by `./manage.py startapp accounts` and add it to `INSTALLED_APPS` setting.
2. Build the custom User model and manager.
   `accounts/models.py`

   ```python
   from django.contrib.auth.base_user import BaseUserManager
   from django.db import models
   from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

   # https://www.youtube.com/watch?v=SFarxlTzVX4

   # Model managers


   class MyAccountManager(BaseUserManager):

       def create_user(self, email, username, password=None):
           if not email:
               raise ValueError("Users must have an email address.")
           if not username:
               raise ValueError("Users must have a username.")
           user = self.model(
               email=self.normalize_email(email),  # make email case-insensitive
               username=username
           )
           user.set_password(password)
           user.save(using=self._db)
           return user

       # Used to create the superuser
       def create_superuser(self, email, username, password):
           user = self.create_user(
               email=self.normalize_email(email),  # make email case-insensitive
               username=username,
               password=password
           )
           user.is_admin = True
           user.is_staff = True
           user.is_superuser = True

           user.save(using=self._db)
           return user


   class Account(AbstractBaseUser):

       email = models.EmailField(verbose_name="email", max_length=60, unique=True)
       username = models.CharField(max_length=30, unique=True)
       date_joined = models.DateTimeField(
           verbose_name="date joined", auto_now_add=True)
       last_login = models.DateTimeField(
           verbose_name="last login", auto_now_add=True)

       # Mandatory fields by Django
       is_admin = models.BooleanField(default=False)
       is_active = models.BooleanField(default=True)
       is_staff = models.BooleanField(default=False)
       is_superuser = models.BooleanField(default=False)

       # Tie account manager to the account class
       objects = MyAccountManager()

       # Login with email instead of username
       USERNAME_FIELD = 'email'
       # username is also required when creating user
       REQUIRED_FIELDS = ['username']

       # represent account with username
       def __str__(self):
           return self.username

       # which field to use to give permission
       def has_perm(self, perm, obj=None):
           return self.is_admin

       # Give permission to all users to use all Django app
       def has_module_perms(self, app_label):
           return True

   ```

3. Set the newly built `Account` model as the `AUTH_USER_MODEL` inside `settings.py`

   ```python
   # Specify the model to use for authentication
   AUTH_USER_MODEL = "accounts.Account"
   ```

4. If you used `User` model inside any `models.py`, `serializers.py`, or `views.py`, override it with the custom model specified as `AUTH_USER_MODEL`

   `base/models.py`

   ```python
   from django.contrib.auth import get_user_model
    User = get_user_model()
   ```

5. Add and register `AccountAdmin` class inside `admin.py`. This will display `Accounts` table on the Django admin panel. (The default User table is not available since we're using Account as our auth model)

   `accounts/admin.py`

   ```python
   from django.contrib import admin
   from django.contrib.auth.admin import UserAdmin

   from accounts.models import Account


   class AccountAdmin(UserAdmin):
       list_display = ('email', 'username', 'date_joined',
                       'last_login', 'is_admin', 'is_staff')
       search_fields = ('email', 'username')
       readonly_fields = ('id', 'date_joined', 'last_login')

       # Set filters to nothing to silence the error messages
       filter_horizontal = ()
       list_filter = ()
       fieldsets = ()


   admin.site.register(Account, AccountAdmin)

   ```

6. Add a ModelBackend to make login email case-insensitive

   `accounts/backends.y`

   ```python
   from django.contrib.auth import get_user_model
   from django.contrib.auth.backends import ModelBackend


   class CaseInsensitiveModelBackend(ModelBackend):

       def authenticate(self, request, username=None, password=None, **kwargs):
           UserModel = get_user_model()
           if username is None:
               # Get the username from Account.USERNAME_FIELD
               username = kwargs.get(UserModel.USERNAME_FIELD)

           try:
               # TODO: understand what is going on here
               case_insensitive_username_field = '{}__iexact'.format(
                   UserModel.USERNAME_FIELD)
               user = UserModel._default_manager.get(
                   **{case_insensitive_username_field: username})
           except UserModel.DoesNotExist:
               UserModel().set_password(password)
           else:
               if user.check_password(password) and self.user_can_authenticate(user):
                   return user

   ```

   Then add the backend to the `settings.py`

   ```python
   # Specify the model to use for authentication
   AUTH_USER_MODEL = "accounts.Account"
   # Connect the created backends
   AUTHENTICATION_BACKENDS = (
       'django.contrib.auth.backends.AllowAllUsersModelBackend',
       'accounts.backends.CaseInsensitiveModelBackend'
   )


   ```

7. If you have the existing database, you might need to reset it.
   From Django Documentation

   > Changing AUTH_USER_MODEL after you’ve created database tables is significantly more difficult since it affects foreign keys and many-to-many relationships, for example.
   > This change can’t be done automatically and requires manually fixing your schema, moving your data from the old user table, and possibly manually reapplying some migrations. See #25313 for an outline of the steps.
   > Due to limitations of Django’s dynamic dependency feature for swappable models, **the model referenced by AUTH_USER_MODEL must be created in the first migration of its app (usually called 0001_initial); otherwise, you’ll have dependency issues.**
   > In addition, you may run into a CircularDependencyError when running your migrations as Django won’t be able to automatically break the dependency loop due to the dynamic dependency. If you see this error, you should break the loop by moving the models depended on by your user model into a second migration. (You can try making two normal models that have a ForeignKey to each other and seeing how makemigrations resolves that circular dependency if you want to see how it’s usually done.)

   **The best way to tackle this is to drop the table and remove all migration files and then re run the migrations with your newly made custom model. Hope this will work.**

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
- [Django Log In with Email not Username](https://learndjango.com/tutorials/django-log-in-email-not-username)

- [Custom User Model with email login (DJANGO)
  ](https://youtu.be/SFarxlTzVX4)
