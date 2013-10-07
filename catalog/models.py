from django.db import models

class Category(models.Model):
	chpu = models.CharField(max_length=100, unique=True)	
	name = models.CharField(max_length=100)

class Catalog(models.Model):
	chpu = models.CharField(max_length=100, unique=True)
	name = models.CharField(max_length=100)
	price = models.CharField(max_length=100)
	img = models.CharField(max_length=100)
	about = models.TextField(max_length=500)
	url = models.CharField(max_length=30)
	category = models.ForeignKey(Category)