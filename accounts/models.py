from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager

class UserManager(BaseUserManager):

    def create_user(
        self,
        mobile_number,
        password=None,
        **extra_fields
    ):

        if not mobile_number:
            raise ValueError('Mobile number is required')

        user = self.model(
            mobile_number=mobile_number,
            **extra_fields
        )

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(
        self,
        mobile_number,
        password=None,
        **extra_fields
    ):

        extra_fields.setdefault('is_staff', True)

        extra_fields.setdefault('is_superuser', True)

        return self.create_user(
            mobile_number,
            password,
            **extra_fields
        )

class User(AbstractUser):

    username = None
    mobile_number = models.CharField(max_length=10,unique=True)
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'mobile_number'

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.mobile_number
    