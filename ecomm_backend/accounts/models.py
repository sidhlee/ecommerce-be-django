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
