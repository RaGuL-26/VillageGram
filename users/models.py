from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.text import slugify
import hashlib


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Enter a valid email')
        if not username:
            raise ValueError('Enter a correct username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, dob=None):
        user = self.create_user(
            email=email,
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    slug = models.SlugField(unique=True, blank=True)

    date_join = models.DateTimeField(auto_now_add=True)
    last_login = models.DateField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = f"{self.username}-{self.email}"
            self.slug = slugify(base_slug)
        
            original_slug = self.slug
            queryset = User.objects.filter(slug=self.slug).exists()
            counter = 1
            while queryset:
                self.slug = f"{original_slug}-{hashlib.md5((self.email + str(counter)).encode()).hexdigest()[:5]}"
                queryset = User.objects.filter(slug=self.slug).exists()
                counter += 1

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    
    