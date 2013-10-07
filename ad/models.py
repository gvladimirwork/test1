from django.db import models

class ad(models.Model):
	login = models.CharField(max_length=100, unique=True)
	password = models.CharField(max_length=30)
	