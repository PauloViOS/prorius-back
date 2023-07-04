from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class ProfileManager(BaseUserManager):
	def create_user(self, email, password=None, username=None, name=None):
		if not email or not password:
			raise ValueError('Tanto email quanto nome de usuário são necessários')
		email = self.normalize_email(email)
		user = self.model(email=email, username=username, name=name)
		user.set_password(password)
		user.save()
		return user

	def create_superuser(self, email, password=None, username=None, name=None):
		if not email or not password:
			raise ValueError('Tanto email quanto nome de usuário são necessários')
		user = self.create_user(email, password, username, name)
		user.is_superuser = True
		user.is_staff = True
		user.save()
		return user


class Profile(AbstractBaseUser, PermissionsMixin):
	profile_id = models.AutoField(primary_key=True)
	email = models.EmailField(max_length=50, unique=True)
	username = models.CharField(max_length=50, unique=True)
	name = models.CharField(max_length=50)
	is_deleted = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username', 'name']

	objects = ProfileManager()

	def __str__(self):
		return self.username

