from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class AllUsersManager(BaseUserManager):
    def create_user(self, phone, name, password=None, email=None):
        if not phone:
            raise ValueError("Users must have a phone number")
        
        user = self.model(phone=phone, name=name, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, name, password):
        user = self.create_user(phone=phone, name=name, password=password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class AllUsers(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    is_registered = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = AllUsersManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f"{self.name} ({'Registered' if self.is_registered else 'Contact'})"

    @property
    def is_staff(self):
        return self.is_admin
