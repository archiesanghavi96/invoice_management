from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)


class UserManager(BaseUserManager):
    def create_user(self, email, is_manager, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")

        if not is_manager:
            raise ValueError("Users is manager or not?")

        user_obj = self.model(
            email = self.normalize_email(email),
            is_manager=is_manager
        )
        user_obj.set_password(password) # change user password
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.is_active = is_active
        user_obj.save(using=self._db)
        return user_obj


    def create_superuser(self, email, is_manager, password=None):
        user = self.create_user(
                email,
                is_manager=True,
                password=password,
                is_staff=True,
                is_admin=True
        )
        return user

class User(AbstractBaseUser):
    email       = models.EmailField(max_length=255, unique=True)
    is_manager   = models.BooleanField(default=False)
    is_active   = models.BooleanField(default=True) # can login 
    staff       = models.BooleanField(default=False) # staff user non superuser
    admin       = models.BooleanField(default=False) # superuser 
    timestamp   = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['is_manager']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.is_admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        return self.admin


class items(models.Model):
    name = models.CharField(max_length=100,unique=True)
    description = models.CharField(max_length=100)
    available_quantity = models.IntegerField()
    rate = models.FloatField()
    
    def __str__(self):
        return self.name


class invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=100)
    vendor_name = models.CharField(max_length=250)
    invoice_date = models.DateField(null=True,blank=True)
    pdf = models.FileField()
    item = models.ManyToManyField(items)

    def __str__(self):
        return self.invoice_no
