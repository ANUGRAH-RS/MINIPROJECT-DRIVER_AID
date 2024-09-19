from django.db import models

# Create your models here.
class login_table(models.Model):
    username=models.CharField(max_length=90)
    password=models.CharField(max_length=90)
    type=models.CharField(max_length=90)



class Driver(models.Model):
    LOGIN=models.ForeignKey(login_table,on_delete=models.CASCADE)
    name=models.CharField(max_length=90)
    contact=models.CharField(max_length=90)
    address=models.CharField(max_length=90)
    email=models.CharField(max_length=90)
    licence=models.CharField(max_length=90)
    image=models.FileField()
    # vehicle=models.CharField(max_length=90)
    # vehicletype=models.CharField(max_length=90)
    status=models.CharField(max_length=90)

class User(models.Model):
    LOGIN=models.ForeignKey(login_table,on_delete=models.CASCADE)
    name=models.CharField(max_length=90)
    contact=models.CharField(max_length=90)
    address=models.CharField(max_length=90)
    email=models.CharField(max_length=90)
    city=models.CharField(max_length=90)
    image=models.CharField(max_length=90)
