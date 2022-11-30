from django.contrib.auth.models import AbstractBaseUser, BaseUserManager #type:ignore
from django.db import models

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError("Email address is required")
        if not username:
            raise ValueError("User name is required")
        
        # For create new user:
        user = self.model(
            email=self.normalize_email(email=email), # Convert email to normal
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email=email), 
            username=username, 
            password=password,
            first_name=first_name, 
            last_name=last_name,
        )
        user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.is_superadmin=True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique = True)
    email = models.EmailField(max_length=100, unique = True)
    phone_number = models.CharField(max_length=12)

    # Required for user login/register
    date_joined = models.DateTimeField(auto_now_add = True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email' # Field required when login
    REQUIRED_FIELDS = ['username','first_name', 'last_name'] # Fields required when register, default form is have gmail, password
    # get_all_permissions = True
    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin 

    def has_module_perms(self, add_label):
        return True

    def full_name(self):
        return self.first_name + ' ' + self.last_name


