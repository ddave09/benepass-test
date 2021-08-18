from django.db import models
from django.db.models.base import Model

# Create your models here.

class Machine(models.Model):
    user = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    password = models.CharField(max_length=10000)

class Commands(models.Model):
    command = models.CharField(max_length=10000)

class Result(models.Model):
    machine = models.CharField(max_length=100)
    command = models.CharField(max_length=100)
    output = models.TextField()
    error = models.TextField()
