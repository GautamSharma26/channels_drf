from django.db import models
from .manager import UserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractBaseUser


# Create your models here.
class User(AbstractBaseUser):
    """
    Use of AbstractBaseUser for customize User as per our requirements.
    """
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    '''
    adding custom fields if we need.
    '''
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_no = PhoneNumberField(null=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_delivery_boy = models.BooleanField(default=False)
    is_shop_owner = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'  # this field is for login purpose
    REQUIRED_FIELDS = ['phone_no']

    def __str__(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        # "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
