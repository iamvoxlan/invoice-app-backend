from django.db import models
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.

class UsersManager(BaseUserManager):
    def create_user(self, username, role, password):
        user = self.model(
            username = username,
            role = role
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

class Users(AbstractBaseUser):
    ROLES = (
        ('S', 'Staff'),
        ('L', 'Lead'),
        ('D', 'Director'),
    )

    username = models.CharField(max_length=255, unique=True, null=False)
    role = models.CharField(max_length=1, choices=ROLES)
    
    objects = UsersManager()

    USERNAME_FIELD = 'username'
    REQUIRE_FIELDS = ['username']

    class Meta:
        db_table = 'users'

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh' : str(refresh),
            'access' : str(refresh.access_token)
        }