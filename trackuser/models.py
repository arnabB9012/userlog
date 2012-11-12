from django.db import models

class User(models.Model):
	username = models.CharField(max_length=200)
	password = models.CharField(max_length=50)

class Login(models.Model):
	user = models.ForeignKey(User)
	loginlast = models.DateTimeField()


