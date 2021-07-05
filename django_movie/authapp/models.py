from django.db import models
from django.contrib.auth.models import AbstractUser




class User(AbstractUser):

    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d/', verbose_name='аватар', blank=True)


    def __str__(self):
        return f"{self.username}"

