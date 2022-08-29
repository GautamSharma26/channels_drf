from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.password_validation import get_password_validators, validate_password
from django.core.exceptions import ValidationError
from rest_framework import exceptions
from pizza import settings


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, password2=None, **other_fields):
        """
        Creates and saves a User with the given email,password and extra fields which are given User model.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            **other_fields
        )
        try:
            # validate the password against existing validators
            validate_password(
                password,
                password_validators=get_password_validators(settings.AUTH_PASSWORD_VALIDATORS)
            )
        except ValidationError as e:
            # raise a validation error
            raise exceptions.ValidationError({
                'password': e.messages
            })

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, password2=None, **other_fields):
        """
        Creates and saves a superuser with the given email,phone_no(required fields),and password.
        """
        user = self.create_user(
            email,
            password=password,
            **other_fields

        )
        user.is_admin = True
        user.save(using=self._db)
        return user

