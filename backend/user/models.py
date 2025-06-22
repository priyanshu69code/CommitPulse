from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from core.models import Core
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None  # Remove the username field
    email = models.EmailField(unique=True)  # Use email as the unique identifier
    first_name = models.CharField(max_length=30, blank=True)  # Optional first name
    last_name = models.CharField(max_length=30, blank=True)  # Optional last


    USERNAME_FIELD = 'email'  # Set email as the username field
    REQUIRED_FIELDS = []  # No required fields other than email

    objects = UserManager()  # Use the custom user manager

    def __str__(self):
        return self.email  # Return email as string representation of the user


class GitHubTokern(Core):
    """
    Model to store GitHub Personal Access Tokens for users.
    This allows users to authenticate with GitHub and access their data.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='github_token')
    token = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.user.email} - GitHub Token"
