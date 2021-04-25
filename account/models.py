from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomUser(AbstractUser):
    """
    override Abstract User Model for future customization
    ex: email authentication
    """
    pass
