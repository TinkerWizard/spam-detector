from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from core.models import AllUsers
from django.dispatch import receiver
from django.db.models.signals import post_save

class UserManager(BaseUserManager):
    def create_user(self, name, phone, email, password=None):
        if not phone:
            raise ValueError('Users must have a phone number')
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(name=name, phone=phone, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.BigIntegerField(unique=True, null=False)
    email = models.EmailField(blank=True)

    # last_login is not needed. so, it is set to none.
    last_login = None
    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f"Name: {self.name}, Phone: {self.phone}"


@receiver(post_save, sender=User)
def create_all_users_entry(sender, instance, created, **kwargs):
    if created:
        AllUsers.objects.create(
            name=instance.name,
            phone=instance.phone,   
            email=instance.email,
            is_registered=True
        )